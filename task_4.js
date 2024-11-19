// import csv file, convert to json, 1-50k, each variable named, range between all valuesin each variable, give weight based on value of variable, given each diamond randomly, adjust weights and bias based on error
const minPrice = 200;
const maxPrice = 30000;
const csv = require('csv-parser')
const fs = require('fs')
const results = {diamonds: []};
const population = []

//cant be a binary string for the population
const population_size = 50;
const generations = 1000;

const cutArray = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'];
const colourArray = ['J', 'I', 'H', 'G', 'F', 'E', 'D'];
const clarityArray = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'];

function dotProduct(v1, v2) {
  let result = 0;
  console.log(v1);
  console.log(v2);
  for(let i = 0; i < v1.length; i++){
    result += v1[i] * v2[i];
    console.log(result);
  }
  return result;
}

// class diamond_NN {
  // const derivativeArr = []; //initialise the derivative array
  // const W = [];
  // function generate_population(population_size){
  //   for(let i = 0; i < population_size; i++) {
  //     const randCarat = Math.random()*5.01;
  //     const randX = Math.random()*10.74;
  //     const randY = Math.random()*58.9;
  //     const randZ = Math.random()*31.8;
  //     const randDepth = 2*randZ/(randX+randY);
  //     const randTable = (Math.random()*52)+43;
  //     population[i] = {carat: randCarat.toFixed(2), cut: cutArray[Math.floor(Math.random()*5)], colour: colourArray[Math.floor(Math.random()*7)], clarity: clarityArray[Math.floor(Math.random()*8)], depth: randDepth.toFixed(2), x: randX.toFixed(2), y: randY.toFixed(2), z: randZ.toFixed(2), table: randTable.toFixed(1)};
  //   }
  //   console.log(population);
  // }
  
  //make the layers
  //random weights at the start, backpropogation then changes the weights
//   function init(X, HL, Y){
//     const L = [X, HL, HL, Y];
//     // console.log(L);
//     for(let i = 0; i < L.length - 1; i++){
//       const w=[Math.random(), Math.random()]
//       W.push(w);
//     }
//     // for(let i = 0; i < L.length - 1; i++){
//     //   const d = [0, 0];
//     //   derivativeArr.push(d);
//     // }
//   }

//   function FF(x){
//     let out = [1,2];
//     for(let i = 0; i < W.length; i++){
//       const Xnext = dotProduct(out, W[i]);
//       out = sigmoid(Xnext);

//     }
//   }

//   init(2,2,2);
// FF();
// }


// function csv_Parse() {
//   fs.createReadStream('data.csv')
//   .pipe(csv())
//   .on('data', (data) => results.diamonds.push(data))
//   .on('end', () => {
//     // console.log(results.diamonds);
//     console.log('ok');
//   });
// }

<<<<<<< HEAD
// // generate_population(population_size);
// csv_Parse();
// diamond_NN();
=======
// generate_population(population_size);
csv_Parse();
// init(2, [2,2], 2);
>>>>>>> a598dbf5210f714497f4fa5fcaab865f413f5851
