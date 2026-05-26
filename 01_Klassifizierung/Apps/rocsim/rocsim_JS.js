let dataSets = {
  dataset1: Array.from({ length: 40 }, (_, i) => ({
    value: i / 39,
    label: i < 20 ? "negativ" : "positiv",
    yJitter: -5 + Math.random() * 160,
  })),
};

let currentDataset = dataSets.dataset1;
let thresholdSlider;
let threshold = 0.5;
let rocCurvePoints = [];

let margin = 40;
let padding = 20;
let Width = 400;
let scale = 40;

const minX = 520;
const maxX = 920;
const baseY = 150;

function setup() {
  createCanvas(1000, 485);

  let header = createP("ROC-Demo | V1.1");
  header.style("font-size", "20px");
  header.style("color", "#800000");
  header.style("font-family", "sans-serif");
  header.style("font-weight", "bold");
  header.position(520, 0);

  let abstr = createP();
  abstr.html(
      "Thomas Joerg (thomas.joerg@bw.schule) & ChatGPT 5.2"
  );
  abstr.style("font-size", "16px");
  abstr.style("color", "#000000");
  abstr.style("font-family", "sans-serif");
  abstr.style("font-weight", "normal");
  abstr.position(520, 35);

  thresholdSlider = createSlider(0, 1, threshold, 0.01);
  thresholdSlider.position(510, 120);
  thresholdSlider.style("width", "415px");

  calculateROC();
}

function draw() {
  background(220);
  threshold = thresholdSlider.value();

  makeCoord(Width, margin, padding, scale);
  drawROCCurve();
  draw1DData();
  drawConfusionTable();
}

function mousePressed() {
  currentDataset.forEach((point) => {
    let x = map(point.value, 0, 1, minX, maxX);
    let y = baseY + point.yJitter;

    if (dist(mouseX, mouseY, x, y) < 8) {
      point.label = point.label === "positiv" ? "negativ" : "positiv";
      calculateROC();
    }
  });
}

function calculateROC() {
  rocCurvePoints = [];
  let steps = 100;

  for (let t = 0; t <= 1.0001; t += 1 / steps) {
    let { TPR, FPR } = calculateMetrics(t);
    rocCurvePoints.push({ TPR, FPR });
  }
}

function calculateMetrics(t) {
  let TP = 0,
    FP = 0,
    TN = 0,
    FN = 0;

  currentDataset.forEach((point) => {
    if (point.value >= t && point.label === "positiv") TP++;
    if (point.value >= t && point.label === "negativ") FP++;
    if (point.value < t && point.label === "negativ") TN++;
    if (point.value < t && point.label === "positiv") FN++;
  });

  let TPR = TP + FN === 0 ? 0 : TP / (TP + FN);
  let FPR = FP + TN === 0 ? 0 : FP / (FP + TN);

  return { TP, FP, TN, FN, TPR, FPR };
}

function drawROCCurve() {
  push();
  noFill();
  stroke(255, 0, 0);
  strokeWeight(2);

  beginShape();
  rocCurvePoints.forEach((p) => {
    let x = map(p.FPR, 0, 1, 40, 440);
    let y = map(p.TPR, 0, 1, 440, 40);
    vertex(x, y);
  });
  endShape();

  fill(0);
  noStroke();
  textSize(16);
  push();
  translate(25, 240); // Position der Beschriftung
  rotate(-HALF_PI); // -90 Grad (gegen den Uhrzeigersinn)
  text("TPR", -15, 431);
  pop();
  text("FPR", 230, 456);
  pop();
}

function draw1DData() {
  let sx = map(threshold, 0, 1, minX, maxX);

  noStroke();
  fill(255, 0, 0, 50);
  rect(sx, baseY - 15, maxX - sx+6, 185);

  fill(0, 0, 255, 50);
  rect(minX-6, baseY - 15, sx - minX+6, 185);

  currentDataset.forEach((point) => {
    let x = map(point.value, 0, 1, minX, maxX);
    let y = baseY + point.yJitter;

    fill(
      point.label === "positiv" ? color(255, 0, 0, 180) : color(0, 0, 255, 180)
    );
    ellipse(x, y, 10, 10);

    fill(0);
    text(point.label === "positiv" ? "+" : "-", x - 3, y + 15);
  });

  stroke(0);
  line(sx, baseY - 25, sx, baseY + 170);

  noStroke();
  fill(0);
  textSize(16);
  text(`Threshold: ${threshold.toFixed(2)}`, sx - 55, baseY - 38);
}

function drawConfusionTable() {
  let { TP, FP, TN, FN, TPR, FPR } = calculateMetrics(threshold);

  push();
  fill(0);
  textSize(16);
  text("True Positives (TP): ", 520, 365);
  text(TP, 680, 365);
  text(`False Negatives (FN):`, 520, 390);
  text(FN, 680, 390);
  text(`True Positive Rate (TPR):`, 720, 365);
  text(`TPR = TP/(TP+FN) = ${TPR.toFixed(2)}`, 720, 390);

  text(`False Positives (FP):`, 520, 435);
  text(FP, 680, 435);
  text(`True Negatives (TN):`, 520, 460);
  text(TN, 680, 460);
  text(`False Positive Rate (FPR):`, 720, 435);
  text(`FPR = FP/(FP+TN) = ${FPR.toFixed(2)}`, 720, 460);

  let px = map(FPR, 0, 1, 40, 440);
  let py = map(TPR, 0, 1, 440, 40);
  ellipse(px, py, 10, 10);
  pop();
}

function makeCoord(Width, margin, padding, scale) {
  fill(255);
  noStroke();
  rect(
    margin - padding,
    margin - padding,
    Width + 2 * padding,
    Width + 2 * padding
  );

  fill(80);
  textSize(13);

  for (let i = 0; i <= Width / scale; i++) {
    stroke(200);
    line(margin, margin + i * scale, Width + padding * 2, margin + i * scale);
    line(margin + i * scale, margin, margin + i * scale, Width + padding * 2);

    noStroke();
    if (i % 2 === 0) {
      text(i / 10, margin + i * scale - 5, Width + padding * 2 + 15);
      if (i == 10) {
        text("1.0", margin + 380, Width + margin - i * scale + 15);
      } else {
        text(i / 10, margin + 380, Width + margin - i * scale - 5);
      }
    }
  }
}
