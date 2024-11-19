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


function diamond_NN() {
  const derivativeArr = []; //initialise the derivative array
  function generate_population(population_size){
    for(let i = 0; i < population_size; i++) {
      const randCarat = Math.random()*5.01;
      const randX = Math.random()*10.74;
      const randY = Math.random()*58.9;
      const randZ = Math.random()*31.8;
      const randDepth = 2*randZ/(randX+randY);
      const randTable = (Math.random()*52)+43;
      population[i] = {carat: randCarat.toFixed(2), cut: cutArray[Math.floor(Math.random()*5)], colour: colourArray[Math.floor(Math.random()*7)], clarity: clarityArray[Math.floor(Math.random()*8)], depth: randDepth.toFixed(2), x: randX.toFixed(2), y: randY.toFixed(2), z: randZ.toFixed(2), table: randTable.toFixed(1)};
    }
    console.log(population);
  }
  
  //make the layers
  //random weights at the start, backpropogation then changes the weights
  function init(X, HL, Y){
    const L = [X, HL, Y];
    const W = [];
    console.log(L);
    for(let i = 0; i < L.length - 1; i++){
      const w=[Math.random(), Math.random()]
      W.push(w);
    }
    // for(let i = 0; i < L.length - 1; i++){
    //   const d = [0, 0];
    //   derivativeArr.push(d);
    // }
  }

}


function csv_Parse() {
  fs.createReadStream('data.csv')
  .pipe(csv())
  .on('data', (data) => results.diamonds.push(data))
  .on('end', () => {
    // console.log(results.diamonds);
    console.log('ok');
  });
}

// generate_population(population_size);
csv_Parse();
// init(2, [2,2], 2);