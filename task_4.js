// import csv file, convert to json, 1-50k, each variable named, range between all valuesin each variable, give weight based on value of variable, given each diamond randomly, adjust weights and bias based on error

const maxcarat = 545.65;
const csv = require('csv-parser')
const fs = require('fs')
const results = {diamonds: []};
const population = []

//cant be a binary string for the population
const population_size = 50;
const generations = 1000;
const crossover_rate = 0.8;
const mutation_rate = 0.01;

const rand = Math.random()*545.65
console.log(rand.toFixed(2));

function generate_population(population_size){
  for(let i = 0; i < population_size; i++) {
    population[i] = {carat: Math.round(Math.random()*545.65), cut: }
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

csv_Parse();