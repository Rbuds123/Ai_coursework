import 'https://cdn.jsdelivr.net/npm/chart.js';
import { generations, PARAMETERS } from './task2.mjs';

const chart = new Chart(
  document.querySelector('canvas'),
  {
    type: 'line',
    options: {
      animation: false,
      maintainAspectRatio: false, // Magically fixes a particular bug.
      plugins: {
        legend: {
          display: false,
        },
        title: {
          text: 'Fitness over time',
          display: true,
        },
      },
      scales: {
        y: {
          // If the data sits outside these values, the chart is allowed to expand.
          suggestedMin: 1600,
          suggestedMax: 2400,
        }
      }
    },
    data: {
      labels: Array.from({ length: PARAMETERS.generations }, (_, k) => k),
      datasets: [
        {
          label: 'mean',
          data: []
        },
        {
          label: 'max',
          data: []
        },
        {
          label: 'median',
          data: []
        }
      ]
    }
  }
);

const generationIterator = generations();
const circle = document.querySelector('.timer circle');

function runGeneration() {
  const { value, done } = generationIterator.next();
  if (!done) {
    const [max, mean, median] = value;

    // Add fitness to chart
    chart.data.datasets.at(0).data.push(mean);
    chart.data.datasets.at(1).data.push(max.at(1));
    chart.data.datasets.at(2).data.push(median.at(1));

    chart.update();
  } else {
    circle.classList.add("finished");
  }
}

document.querySelector('.timer > circle').addEventListener('animationiteration', runGeneration);