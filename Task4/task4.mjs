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

function randomArray(length) {
  return Array.from({length}, Math.random);
}

class DiamondNN {
  constructor(inputs, hiddenLayers = 2, outputs = 1) {
    this.inputs = inputs;
    this.hiddenLayers = hiddenLayers;
    this.outputs = outputs;

    // Based on a suggestion from https://www.linkedin.com/pulse/choosing-number-hidden-layers-neurons-neural-networks-sachdev/
    const hiddenLayerWidth = Math.ceil(Math.sqrt(inputs * outputs));
    
    // Generate a matrix with random values matching the shape of the NN.
    const matrix = [];
    matrix.push(randomArray(inputs));
    for (let layer = 0; layer < hiddenLayers; layer++)
      matrix.push(randomArray(hiddenLayerWidth));
    matrix.push(randomArray(outputs));

    // The random values are the starting weights.
    this.weights = matrix;

    // The random values will be overwritten within the layers matrix.
    this.layers = structuredClone(matrix);
  }
}

const network = new DiamondNN(10);
