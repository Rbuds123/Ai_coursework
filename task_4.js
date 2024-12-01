//import csv file, convert to json, 1-50k, each variable named, range between all valuesin each variable, give weight based on value of variable, given each diamond randomly, adjust weights and bias based on error
const minPrice = 200;
const maxPrice = 30000;
const csv = require('csv-parser')
const fs = require('fs')
const results = [];
const population = []

//cant be a binary string for the population
const population_size = 50;
const generations = 1000;

const cutArray = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'];
const colourArray = ['J', 'I', 'H', 'G', 'F', 'E', 'D'];
const clarityArray = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'];

function dotProduct(v1, v2) {
  let result = 0;
  for (let i = 0; i < v1.length; i++) {
    result += v1[i] * v2[i];
  }
  return result;
}

class diamond_NN {
  constructor(X, HL, Y) {
    this.X = X;
    this.HL = HL;
    this.Y = Y;
    const L = [X, HL, HL, Y];
    const W = [];
    this.derivativeArr = new Array(L.length).fill(0);
    this.out = [];
    for (let i = 0; i < L.length - 1; i++) {
      const w = [Math.random(), Math.random()]
      W.push(w);
      this.W = W;
    }
  }
  static generate_population(population_size) {
    for (let i = 0; i < population_size; i++) {
      const randCarat = Math.random() * 5.01;
      const randX = Math.random() * 10.74;
      const randY = Math.random() * 58.9;
      const randZ = Math.random() * 31.8;
      const randDepth = 2 * randZ / (randX + randY);
      const randTable = (Math.random() * 52) + 43;
      population[i] = { carat: randCarat.toFixed(2), cut: cutArray[Math.floor(Math.random() * 5)], colour: colourArray[Math.floor(Math.random() * 7)], clarity: clarityArray[Math.floor(Math.random() * 8)], depth: randDepth.toFixed(2), x: randX.toFixed(2), y: randY.toFixed(2), z: randZ.toFixed(2), table: randTable.toFixed(1) };
    }
    console.log(population);
  }

  //make the layers
  //random weights at the start, backpropogation then changes the weights
  // init(X, HL, Y) {
  //   this.X = X;
  //   const L = [X, HL, HL, Y];
  //   const derivativeArr = []; //initialise the derivative array
  //   const W = [];
  //   for (let i = 0; i < L.length - 1; i++) {
  //     const w = [Math.random(), Math.random()]
  //     W.push(w);
  //     this.W = W;
  //   }
  //   for (let i = 0; i < L.length - 1; i++) {
  //     const d = [0, 0];
  //     derivativeArr.push(d);
  //     this.derivativeArr = derivativeArr;
  //   }
  // }

  FF(x) {
    let out = x;
    this.out[0];
    for (let i = 0; i < this.W.length; i++) {
      const Xnext = dotProduct(out, this.W[i]);
      out = this.sigmoid(Xnext);
      this.out[i+1] = out;
    }
    return out;
  }

  BackPropogate(error) {
    for(let i = this.derivativeArr.length-1; i <= 0; i--){
      const out = this.out[i+1];
      const delta = error * this.sigmoid_Derivative(out);
      const fixed_delta = [];
      for(let i = 0; i < delta.length; i++){
        fixed_delta.push([delta[i]]);
      }
      let current_Out = this.out[i];
      let column_Out = [];
      column_Out.push([current_Out[i]]);
      // for(let i = 0; i < current_Out.length; i++){
      //   column_Out.push([current_Out[i]]);
      // }
      this.derivativeArr[i] = dotProduct(column_Out, fixed_delta);
      error = dotProduct(delta, this.W);
    }
  }

  train_NN(x, target, epochs, lr){
    for(let i = 0; i < epochs; i++){
      let S_errors = 0;
      console.log(i);
      for(let j = 0; j < x.length; i++){
        const t = target[j]
        const output = this.FF(j);
        const e = t - output;
        this.BackPropogate(e);
        this.GD(lr);
        S_errors += this.meanSquareError(t, output);
      }
    }
  }
  
  GD(lr = 0.05) {
    for(let i = 0; i < this.W.length; i++){
      const W = this.W[i];
      const derivativeArr = this.derivativeArr[i];
      this.W += this.derivativeArr*lr;
    }
  }

  sigmoid(x){
    const y=[]
    for(let i = 0; i < x.length; i++){
      y.push(1/(1+Math.E ** -x[i]));
    }
    // y.push(1/(1+Math.E ** -x));
    // console.log(y);
    return y;
  }

  sigmoid_Derivative(x){
    const sig_derivative = [];
    // for(let i = 0; i < x.length; i++){
    //   sig_derivative.push(sig_derivative = x[i] * (1-x[i]))
    // }
    sig_derivative.push(x * (1-x));
    return sig_derivative;
  }

  meanSquareError(t, output){
    let msqe;
    let t_output = [];

    for(let i = 0; i < output.length; i++){
      t_output.push((t-output[i]) ** 2);
    }
    for(let i = 0; i < t_output.length; i++){
      msqe += t_output;
    }
    msqe = msqe/t_output;
    return msqe;
  }
}

function init(){
  const training_inputs = [];
  const targets = [];
  for(let i = 0; i < 1000; i++){
    training_inputs.push(results[Math.random()*53941]);
    targets.push(Math.random()*18823);
  }

  const nn = new diamond_NN(2,5,1);
  nn.train_NN(training_inputs, targets, 10, 0.1);
}


function csv_Parse() {
  fs.createReadStream('data.csv')
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      // console.log(results.diamonds);
      // console.log('ok');
    });
}

//  for(let i = 0; i < L.length - 1; i++){
//   const d = [0, 0];
//   derivativeArr.push(d);
// }

init();
csv_Parse();
