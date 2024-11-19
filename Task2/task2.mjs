const DATA = {
  weights: [3, 8, 2, 9, 7, 1, 8, 13, 10, 9],
  profits: [126, 154, 256, 526, 388, 245, 210, 442, 671, 348],
  capacity: 35,
}

const PARAMETERS = {
  populationSize: 100,
  generations: 25,
  crossoverRate: 0.8,
  mutationRate: 0.02,
  genomeSize: DATA.weights.length,
}

const chart = new Chart(
  document.querySelector('canvas'),
  {
    type: 'line',
    option: {
      animation: false,
    },
    data: {
      labels: Array.from({length: PARAMETERS.generations}, (_, k) => k),
      datasets: [
        {
          label: 'fitness',
          data: []
        }
      ]
    }
  }
);

/**
 * Random binary array where the chance of being a 1 can be altered.
 * @param {Number} chance 
 * @param {int} size 
 * @returns {int[]}
 */
const weightedBinaryArray = (chance = 0.50, size = PARAMETERS.genomeSize) => Array.from({ length: size }, () => +(Math.random() <= chance));

class Individual {
  constructor(genome = weightedBinaryArray()) {
    this.genome = genome;
  }

  get fitness() {
    if (this.weight > DATA.capacity) {
      return 0;
    } else {
      return this.profit;
    }
  }

  get weight() {
    return DATA.weights.reduce((p, c, i) => p + (this.genome.at(i) && c), 0);
  }

  get profit() {
    return DATA.profits.reduce((p, c, i) => p + (this.genome.at(i) && c), 0);
  }

  breed(other) {
    return Individual.crossover(this.genome, other.genome).map(genome => new Individual(Individual.mutate(genome)));
  }

  static crossover(a, b) {
    if (Math.random() < PARAMETERS.crossoverRate) {
      const point = Math.floor(Math.random() * a.length);
      return [a.slice(0, point).concat(b.slice(point)), b.slice(0, point).concat(a.slice(point))];
    }

    return [a, b];
  }

  static mutate(a) {
    // Uses XOR to flip the bit.
    return a.map(v => v ^ (Math.random() < PARAMETERS.mutationRate));
  }
}

let population = Array.from({ length: PARAMETERS.populationSize }, () => {
  const individual = new Individual();
  // I've chosen to copy out the fitness for efficiency - `fittest`,
  // `totalFitness`, and normalising the fitnesses would re-run the
  // fitness function.
  return [individual, individual.fitness];
});

for (let generation = 0; generation < PARAMETERS.generations; generation++) {
  // Sort population, least fit first.
  population.sort((a, b) => a[1] - b[1]);

  // Pull out the fittest member.
  chart.data.datasets.at(0).data.push(population.at(-1).at(1));
  chart.update();

  // Normalise fitnesses
  const totalFitness = population.reduce((p, [_, f]) => p + f, 0);
  let previousProbability = 0;
  for (let i = 0; i < PARAMETERS.populationSize; i++) {
    previousProbability += population[i][1] / totalFitness;
    population[i][1] = previousProbability;
  }

  // Generate next population
  const nextPopulation = [];
  while (nextPopulation.length < PARAMETERS.populationSize) {
    // Pick the two roulette arrows
    const selectorA = Math.random(), selectorB = Math.random();

    // Find the two individuals who are just above the arrow
    const [parentA] = population.find(([_, f]) => f > selectorA);
    const [parentB] = population.find(([_, f]) => f > selectorB);

    // Breed the two individuals
    const [childA, childB] = parentA.breed(parentB);

    // Add them to the new data structure
    nextPopulation.push([childA, childA.fitness], [childB, childB.fitness]);
  }

  population = nextPopulation;
}
