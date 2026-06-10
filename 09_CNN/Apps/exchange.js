// exchange.js - Data and Network Exchange Utilities (CNN Grayscale Trainer)

/**
 * Downloads a file with given content.
 */
export function downloadFile(content, filename, mimeType = 'text/plain') {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Exports an image dataset as CSV: pixel_0, pixel_1, ..., pixel_N, label
 * @param {Array} samples - Array of {input: number[], output: number[] (one-hot)}
 * @param {string[]} outputNames - Class names (one per one-hot position)
 * @returns {string} CSV content
 */
export function exportImageCSV(samples, outputNames) {
    if (!samples.length) return '';
    const pixelCount = samples[0].input.length;
    const headers = [];
    for (let i = 0; i < pixelCount; i++) headers.push('pixel_' + i);
    headers.push('label');

    const rows = samples.map(s => {
        const labelIdx = s.output.indexOf(Math.max(...s.output));
        const label = outputNames[labelIdx] != null ? outputNames[labelIdx] : labelIdx;
        const vals = s.input.map(v => (Math.round(v * 1e6) / 1e6).toString());
        vals.push('"' + label + '"');
        return vals.join(',');
    });

    return [headers.join(','), ...rows].join('\n');
}

/**
 * Exports a CNN to the didactic-cnn-v1 JSON format.
 * @param {Array} network - Flat layer array ([conv?, conv?, dense?, dense?, output])
 * @param {Object} meta - { inputLabels, outputLabels, imageWidth, imageHeight, networkName }
 */
export function exportNetwork(network, meta) {
    if (!network || network.length === 0) {
        throw new Error('No network to export');
    }
    const { inputLabels, outputLabels, imageWidth, imageHeight, networkName } = meta;

    const denseLayers = network.filter(l => l.type === 'dense');
    let convCount = 0, denseCount = 0;

    const layers = network.map((layer) => {
        if (layer.type === 'conv') {
            convCount++;
            return {
                name: 'conv_' + convCount,
                type: 'conv',
                activation: layer.activation,
                pool: layer.pool,
                kernels: layer.kernels.map(k => k.map(c => c.map(r => [...r]))),
                bias: [...layer.biases],
                notes: 'Conv layer ' + convCount + ' with ' + layer.kernels.length + ' kernels.'
            };
        }
        // dense
        const isOutput = layer === denseLayers[denseLayers.length - 1];
        denseCount++;
        const neuronLabels = isOutput
            ? [...outputLabels]
            : Array.from({ length: layer.size }, (_, i) => 'h' + denseCount + '_' + (i + 1));
        return {
            name: isOutput ? 'output' : 'dense_' + denseCount,
            type: 'dense',
            neuron_labels: neuronLabels,
            activation: layer.activation,
            weights: layer.weights.map(w => [...w]),
            bias: [...layer.biases],
            notes: isOutput
                ? 'Output layer with ' + layer.size + ' neurons.'
                : 'Dense hidden layer with ' + layer.size + ' neurons.'
        };
    });

    return {
        format: 'didactic-cnn-v1',
        network_name: networkName || 'custom_cnn',
        image_width: imageWidth,
        image_height: imageHeight,
        input_labels: [...inputLabels],
        output_labels: [...outputLabels],
        layers
    };
}

/**
 * Imports a CNN from didactic-cnn-v1 JSON. Reconstructs the full layer array
 * (with computed feature-map dimensions) plus the architecture descriptor.
 * @param {Object} json
 * @returns {Object} { imageWidth, imageHeight, inputNames, outputNames, arch, network }
 */
export function importNetwork(json) {
    if (json.format === 'didactic-neural-network-v1') {
        throw new Error('Dense network format not supported in CNN mode.');
    }
    if (json.format !== 'didactic-cnn-v1') {
        throw new Error('Unsupported network format');
    }
    if (!json.layers || !json.input_labels || !json.output_labels) {
        throw new Error('Invalid network structure');
    }

    const imageWidth = json.image_width;
    const imageHeight = json.image_height;
    const network = [];
    const archConv = [];
    const archDense = [];

    let inC = 1, inH = imageHeight, inW = imageWidth;
    const denseJsonLayers = json.layers.filter(l => l.type === 'dense');

    for (const layer of json.layers) {
        if (layer.type === 'conv') {
            if (!Array.isArray(layer.kernels) || !Array.isArray(layer.bias)) {
                throw new Error('Invalid conv layer: missing kernels or bias');
            }
            const K = layer.kernels.length;
            const pool = layer.pool || 'none';
            const cH = inH - 2, cW = inW - 2;
            let oH = cH, oW = cW;
            if (pool !== 'none') { oH = Math.floor(cH / 2); oW = Math.floor(cW / 2); }
            network.push({
                type: 'conv',
                kernels: layer.kernels.map(k => k.map(c => c.map(r => [...r]))),
                biases: [...layer.bias],
                activation: layer.activation,
                pool,
                inC, inH, inW,
                convH: cH, convW: cW,
                outC: K, outH: oH, outW: oW
            });
            archConv.push({ kernels: K, activation: layer.activation, pool });
            inC = K; inH = oH; inW = oW;
        } else if (layer.type === 'dense') {
            if (!Array.isArray(layer.weights) || !Array.isArray(layer.bias)) {
                throw new Error('Invalid dense layer: missing weights or bias');
            }
            const size = layer.weights.length;
            const prevSize = layer.weights[0].length;
            network.push({
                type: 'dense',
                weights: layer.weights.map(w => [...w]),
                biases: [...layer.bias],
                activation: layer.activation,
                size,
                prevSize
            });
            const isOutput = layer === denseJsonLayers[denseJsonLayers.length - 1];
            if (!isOutput) archDense.push({ size, activation: layer.activation });
        } else {
            throw new Error('Unknown layer type: ' + layer.type);
        }
    }

    return {
        imageWidth,
        imageHeight,
        inputNames: [...json.input_labels],
        outputNames: [...json.output_labels],
        arch: { convLayers: archConv, denseLayers: archDense },
        network
    };
}
