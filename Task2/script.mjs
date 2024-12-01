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
  const { value: things, done } = generationIterator.next();
  const boxes = document.querySelectorAll(".box");
  const slots = document.querySelectorAll(".boxSlot");
  const fitnessDisplay = document.querySelector('#fitnessDisplay');
  const fittest = things[1];
  let usedSlots = 0;
  if (!done) {
    chart.data.datasets.at(0).data.push(things[0]);
    chart.update();
    for (let i = 0; i < fittest.length; i++) {
      if (fittest[i] == 1) {
        boxes[i].x.baseVal.value = slots[usedSlots].x.baseVal.value;
        boxes[i].y.baseVal.value = slots[usedSlots].y.baseVal.value;
        boxes[i].style = `left: ${slots[usedSlots].x}, top: ${slots[usedSlots].y}`;
        boxes[i].classList.remove('hidden');
        usedSlots += 1;
      } else {
        boxes[i].classList.add('hidden');
      }
    }
    fitnessDisplay.textContent = '£' + things[2] + 'k - ' + things[3] + 'T';
  } else {
    circle.classList.add("finished");
  }
}

document.querySelector('.timer > circle').addEventListener('animationiteration', runGeneration);