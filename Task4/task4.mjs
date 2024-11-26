const CUT = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'];
const COLOUR = ['J', 'I', 'H', 'G', 'F', 'E', 'D'];
const CLARITY = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'];

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

/** Dot product of two arrays */
const dot = (a, b) => a.reduce((p, c, i) => p + c * b[i], 0);

/** Applies a sigmoid activation function to a value */
const sigmoid = v => 1 / (1 + Math.exp(-v));

/**
 * @param {number[][]} layers 
 * @param {Function} from 
 */
function edges(layers, from) {
  // Take a clone to use the original dimensions
  const matrix = structuredClone(layers);

  // Work backwards through the layers
  for (let index = matrix.length-1; index >= 0; index--) {
    // Then fill in the edge array for each node.
    for (const node of matrix[index].keys()) {
      matrix[index][node] = Array.from({length: layers[index-1]?.length}, from);
    }
  }

  return matrix;
}

class DiamondNN {
  constructor(inputs, hiddenLayers = 2, outputs = 1, learningRate = 0.1) {
    this.learningRate = learningRate;

    // Based on a suggestion from https://www.linkedin.com/pulse/choosing-number-hidden-layers-neurons-neural-networks-sachdev/
    const hiddenLayerWidth = Math.ceil(Math.sqrt(inputs * outputs));
    const lengths = [inputs].concat(new Array(hiddenLayers).fill(hiddenLayerWidth)).concat(outputs)

    this.layers = lengths.map(length => Array.from({length}, () => 0));
    this.weights = edges(this.layers, Math.random);
    this.derivatives = edges(this.layers, () => 0);
  }

  /**
   * Trains the neural network on a batch of inputs
   * @param {number[][]} batch 
   */
  train(batch) {
    for (const inputs of batch) {
      this.forward(inputs);
    }
  }

  /** @param {number[]} inputs */
  forward(inputs) {
    // Write the inputs into the matrix
    this.layers[0] = inputs;

    // Work through the hidden layers
    for (let index = 1; index < this.layers.length; index++) {
      // Work through each node of the layer
      for (const node of this.layers[index].keys()) {
        this.layers[index][node] = sigmoid(dot(this.layers[index-1], this.weights[index][node]) + 1);
      }
    }
  }

  get output() {
    return this.layers.at(-1)[0];
  }

  /** @param {number[]} lengths */
  static makeWeights(lengths) {
    const matrix = lengths.map(length => new Array(length));
    for (const [index, layer] of matrix.entries()) {
      for (const node of layer.keys()) {
        if (!matrix[index + 1]) break;
        matrix[index][node] = Array.from({ length: lengths.at(index + 1) ?? 0 }, Math.random);
      }
    }
    return matrix;
  }
}

const network = new DiamondNN(10);

// console.log(structuredClone(network));
network.forward(Array.from({length: 10}, Math.random));
// console.log(structuredClone(network));
console.log(network.output)