// exchange.js - Data and Network Exchange Utilities

/**
 * Exports the current dataset as CSV (using DOT as decimal separator)
 * @param {Array} data - Array of {input: number[], output: number[]}
 * @param {string[]} inputNames - Input column names
 * @param {string[]} outputNames - Output column names
 * @returns {string} CSV content
 */
export function exportCSV(data, inputNames, outputNames) {
    if (!data.length) return '';
    
    const headers = [...inputNames, ...outputNames].join(',');
    const rows = data.map(row => {
        const values = [...row.input, ...row.output].map(v => 
            typeof v === 'number' ? v.toString() : `"${v}"`
        );
        return values.join(',');
    });
    
    return [headers, ...rows].join('\n');
}

/**
 * Downloads a file with given content
 * @param {string} content - File content
 * @param {string} filename - Filename
 * @param {string} mimeType - MIME type
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
 * Exports neural network to didactic JSON format
 * @param {Array} network - Network layers from forward pass
 * @param {string[]} inputNames - Input labels
 * @param {string[]} outputNames - Output labels
 * @param {string} networkName - Network name
 * @returns {Object} Didactic JSON structure
 */
export function exportNetwork(network, inputNames, outputNames, networkName = 'custom_network') {
    if (!network || network.length === 0) {
        throw new Error('No network to export');
    }
    
    const layers = network.map((layer, index) => {
        const isOutputLayer = index === network.length - 1;
        const neuronCount = layer.size;
        
        // Generate neuron labels
        const neuronLabels = isOutputLayer 
            ? outputNames 
            : Array.from({ length: neuronCount }, (_, i) => `h${index + 1}_${i + 1}`);
        
        return {
            name: isOutputLayer ? 'output_layer' : `hidden_layer_${index + 1}`,
            type: 'dense',
            neuron_labels: neuronLabels,
            activation: layer.activation,
            notes: isOutputLayer 
                ? `Output layer with ${neuronCount} neuron${neuronCount !== 1 ? 's' : ''}.`
                : `Hidden layer ${index + 1} with ${neuronCount} neuron${neuronCount !== 1 ? 's' : ''}.`,
            weights: layer.weights.map(w => [...w]), // Deep copy
            bias: [...layer.biases] // Deep copy
        };
    });
    
    return {
        format: 'didactic-neural-network-v1',
        network_name: networkName,
        input_labels: [...inputNames],
        output_labels: [...outputNames],
        layers: layers
    };
}

/**
 * Imports neural network from didactic JSON format
 * @param {Object} json - Imported JSON structure
 * @returns {Object} Network configuration object
 */
export function importNetwork(json) {
    if (json.format !== 'didactic-neural-network-v1') {
        throw new Error('Unsupported network format');
    }
    
    // Validate structure
    if (!json.input_labels || !json.output_labels || !json.layers) {
        throw new Error('Invalid network structure');
    }
    
    const hiddenLayers = [];
    let outputActivation = 'sigmoid';
    
    // Process layers
    for (let i = 0; i < json.layers.length; i++) {
        const layer = json.layers[i];
        const isOutputLayer = i === json.layers.length - 1;
        
        if (isOutputLayer) {
            outputActivation = layer.activation;
        } else {
            hiddenLayers.push({
                size: layer.neuron_labels.length,
                activation: layer.activation
            });
        }
    }
    
    return {
        data: null, // Will be handled separately
        inputNames: [...json.input_labels],
        outputNames: [...json.output_labels],
        hiddenLayers: hiddenLayers,
        outputActivation: outputActivation,
        networkData: json // Full network weights for reconstruction
    };
}

/**
 * Reconstructs network weights from imported JSON
 * @param {Object} network - Current network reference
 * @param {Object} importedData - Imported JSON network data
 */
export function reconstructNetworkWeights(network, importedData) {
    if (!network || !importedData || importedData.layers.length !== network.length) {
        throw new Error('Network structure mismatch');
    }
    
    for (let i = 0; i < network.length; i++) {
        const importedLayer = importedData.layers[i];
        const currentLayer = network[i];
        
        // Validate dimensions
        if (importedLayer.weights.length !== currentLayer.size ||
            importedLayer.bias.length !== currentLayer.size) {
            throw new Error(`Layer ${i} dimension mismatch`);
        }
        
        // Copy weights and biases
        for (let j = 0; j < currentLayer.size; j++) {
            if (importedLayer.weights[j].length !== currentLayer.prevSize) {
                throw new Error(`Weights dimension mismatch in layer ${i}, neuron ${j}`);
            }
            currentLayer.weights[j] = [...importedLayer.weights[j]];
            currentLayer.biases[j] = importedLayer.bias[j];
        }
    }
}
