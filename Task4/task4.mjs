/**
 * A neural network to predict the price of a diamond based on its characteristics.
 */

const CUT = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'];
const COLOUR = ['J', 'I', 'H', 'G', 'F', 'E', 'D'];
const CLARITY = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'];

const EPOCHS = 500;
const BATCH_SIZE = 32;
const LEARNING_RATE = 0.01;

// Load CSV into localStorage, so we can access it by line on-demand.
// Using localStorage this way saves 3s on startup.
if (!localStorage.getItem('data-length')) {
  // Fetch data
  let csv = await fetch(import.meta.resolve('./data.csv'));
  csv = await csv.text();

  // Store data
  csv = csv.split('\n').slice(1);
  for (let i = 0; i < csv.length; i++) {
    // Store the entry in localStorage.
    localStorage.setItem(`data-${i}`, csv.at(i));
  }

  // We've set every single item, we can now mark it done.
  localStorage.setItem('data-length', csv.length);
}

const dot = (a, b) => a.reduce((p, v, i) => p + v * b[i], 0);
const sigmoid = x => 1 / (1 + Math.exp(-x));
const sigmoidDerivative = x => sigmoid(x) * (1 - sigmoid(x));

// const relu = x => Math.max(0, x);
// const reluDerivative = x => (x > 0 ? 1 : 0);|

class Neuron {
  /** An array retaining the input for use in gradient descent @type {number[]} */
  inputs;
  /** The sum before the activation function, to be used with the derivative @type {number[]} */
  weightedSum;
  /** The weights from the previous layer to this neuron @type {number[]} */
  weights;
  /** @type {number} */
  bias;
  /** The final output of the node, post activation function @type {number} */
  output;

  constructor(inputSize, bias = Math.random() * 2 - 1) {
    this.bias = bias;
    // Generate random values from -1 to +1
    this.weights = Array.from({ length: inputSize }, () => Math.random() * 2 - 1);
  }

  activate(inputs) {
    // Store the input to use in gradient descent
    this.inputs = inputs;
    this.weightedSum = this.weights.reduce((total, weight, index) => total + weight * inputs[index], 0) + this.bias;
    // Put the output value through the activation function
    // this.output = sigmoid(this.weightedSum);
    this.output = sigmoid(this.weightedSum);
    return this.output;
  }

  update(learningRate, delta) {
    this.weights = this.weights.map((weight, index) => weight - learningRate * delta * this.inputs[index]);
    this.bias -= learningRate * delta;
  }
}

class DiamondNN {
  /** @type {Neuron[][]} */
  layers = [];

  /** @type {number} */
  learningRate;

  constructor(inputSize, learningRate) {
    this.learningRate = learningRate;

    // Based on a suggestion from https://www.linkedin.com/pulse/choosing-number-hidden-layers-neurons-neural-networks-sachdev/
    const hiddenLayerWidth = ~~(inputSize * .5);

    // A network with two hidden layers.
    const layerSizes = [inputSize, hiddenLayerWidth, hiddenLayerWidth, hiddenLayerWidth, hiddenLayerWidth, 1];

    // Generate neurons for each layer aside from the inputs.
    for (let i = 1; i < layerSizes.length; i++) {
      // Generate a layer with a weight vector with a size corresponding to the size of the outputs of the previous layer.
      this.layers.push(Array.from({ length: layerSizes.at(i) }, () => new Neuron(layerSizes.at(i - 1))));
    }
  }


  train(entry) {
    const [carat, cut, colour, clarity, depth, table, price, x, y, z] = DiamondNN.fetchEntry(entry);
    const [output] = this.forward([carat, cut, colour, clarity, depth, table, x, y, z]);
    this.backward([price]);
    // console.log(output, price)
    return output - price;
  }

  static fetchEntry(entry) {
    let [carat, cut, colour, clarity, depth, table, price, x, y, z] = localStorage.getItem(`data-${entry}`).split(',');

    // Coerce the data types into numbers, using the maximums given in the brief
    // carat = +carat / 6.00;
    // cut = CUT.indexOf(cut) / CUT.length;
    // colour = COLOUR.indexOf(colour) / COLOUR.length;
    // clarity = CLARITY.indexOf(clarity) / CLARITY.length;
    // depth = +depth / 80;
    // table = +table;
    // price = +price / 20_000; // normalise price so it's easier to train for
    // x = +x / 12;
    // y = +y / 60;
    // z = +z / 32;

    carat = +carat;
    cut = CUT.indexOf(cut) / CUT.length;
    colour = COLOUR.indexOf(colour) / COLOUR.length;
    clarity = CLARITY.indexOf(clarity) / CLARITY.length;
    depth = +depth;
    table = +table;
    price = +price / 20_000; // normalise price so it's easier to train for
    x = +x;
    y = +y;
    z = +z;
    
    const output = [carat, cut, colour, clarity, depth, table, price, x, y, z];
    if (output.filter(v => isNaN(v)).length) console.log(entry, localStorage.getItem(`data-${entry}`));
    return [carat, cut, colour, clarity, depth, table, price, x, y, z];
  }
  /**
   * Runs the network forward end-to-end
   * @param {number[]} inputs 
   * @returns {number}
   */
  forward(inputs) {
    // Brilliant trick inspired by https://medium.com/@pat_metzdorf/building-a-basic-neural-net-using-javascript-1f554780dc60
    return this.layers.reduce((input, layer) => layer.map(neuron => neuron.activate(input)), inputs);
  }

  /**
   * Does backpropogation and gradient descent in one go
   * @param {number[]} targets 
   */
  backward(targets) {
    let deltas = this.layers.at(-1).map((neuron, index) => (neuron.output - targets[index]) * sigmoidDerivative(neuron.weightedSum));
    for (let i = this.layers.length - 1; i >= 0; i--) {
      deltas = this.layers.at(i).map((neuron, index) => {
        const delta = sigmoidDerivative(neuron.weightedSum) * deltas.at(index % deltas.length);
        neuron.update(this.learningRate, delta);
        return delta;
      });
    }
  }
}

const network = new DiamondNN(9, LEARNING_RATE);
const DATA_LENGTH = +localStorage.getItem('data-length');

const entry = Math.floor(Math.random()*DATA_LENGTH);
console.log(localStorage.getItem(`data-${entry}`));
console.log(network.train(entry)*20_000);

for (let epoch = 0; epoch < EPOCHS; epoch++) {
  let totalLoss = 0;
  // Pick BATCH_SIZE number of entries from the dataset
  const batch = Array.from({length: BATCH_SIZE}, () => Math.floor(Math.random()*DATA_LENGTH));
  for (let i = 0; i < 3; i++) {
    for (const entry of batch) {
      totalLoss += network.train(entry) ** 2;
    }
  }

  if (epoch % 100 === 0) {
    // console.log(structuredClone(network).layers.at(1).at(1).weights);
    console.log(totalLoss / BATCH_SIZE);
  }
}

console.log(localStorage.getItem(`data-${entry}`));
console.log(network.train(entry)*20_000);
