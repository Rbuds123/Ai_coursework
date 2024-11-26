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
        title: {
          text: 'Fitness over time',
          display: true,
        },
      },
      scales: {
        x: {
          title: {
            text: 'Generation',
            display: true
          }
        },
        y: {
          title: {
            text: 'Fitness',
            display: true
          },
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
        }
      ]
    }
  }
);

const generationIterator = generations();
const circle = document.querySelector('.timer circle');

function runGeneration() {
  const { value: mean, done } = generationIterator.next();
  if (!done) {
    chart.data.datasets.at(0).data.push(mean);
    chart.update();
  } else {
    circle.classList.add("finished");
  }
}

document.querySelector('.timer > circle').addEventListener('animationiteration', runGeneration);