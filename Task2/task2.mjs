const DATA = {
  weights: [3, 8, 2, 9, 7, 1, 8, 13, 10, 9],
  profits: [126, 154, 256, 526, 388, 245, 210, 442, 671, 348],
  capacity: 35,
}

export const PARAMETERS = {
  populationSize: 100,
  generations: 100,
  crossoverRate: 0.8,
  mutationRate: 0.01,
  genomeSize: DATA.weights.length,
}

class Individual {
  constructor(genome) {
    this.genome = genome ?? Array.from({ length: PARAMETERS.genomeSize }, () => +(Math.random() <= .5));
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

export function* generations() {
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

    // Normalise fitnesses
    const totalFitness = population.reduce((p, [_, f]) => p + f, 0);

    // Produce the mean fitness
    yield totalFitness / PARAMETERS.populationSize;

    let cumulativeProbability = 0;
    for (let i = 0; i < PARAMETERS.populationSize; i++) {
      cumulativeProbability += population[i][1] / totalFitness;
      population[i][1] = cumulativeProbability;
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
  return population.at(-1).at(1);
}
