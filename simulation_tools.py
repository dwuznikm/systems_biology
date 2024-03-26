import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os


def random_genotype(n):
  return [random.uniform(-10, 10) for i in range(n)]


def fitness(optimal_genotype, genotype):
    if len(optimal_genotype) != len(genotype):
        raise ValueError("Długość wektorów musi być taka sama.")
    suma_kwadratow_roznicy = sum((a - b)**2 for a, b in zip(optimal_genotype, genotype))
    fitness_value = math.sqrt(suma_kwadratow_roznicy)
    return fitness_value


def mutation(mi, genotype, strenght):
  if np.random.random() < mi:
    p = np.random.normal(loc=0, scale=strenght)
    genotype += p
  return genotype


def calculate_optimal_genotype(mi, genotype, strenght, n):
  if np.random.random() < mi:
    p = np.random.normal(loc=0.3, scale=strenght, size=n)
    genotype += p
  return genotype

def children_roullete(fitness, max_fitness):
  exponent = (max_fitness - fitness)/15
  l = np.exp(exponent)
  children_amount = np.random.poisson(lam=l)
  if children_amount > 3:
    return 3
  else:
    return children_amount

# zmienić z liniowej
def calculate_max_fitness(population):
  return max(15 - population * 0.015, 2)


def create_plot(values, time, subfolder_path, data_type):
  
  life = {'x':[], 'y':[]}
  fig, ax = plt.subplots(figsize=(10, 7))
  
  def update(frame):
      ax.clear()
      life['x'].append(frame)
      life['y'].append(values[frame])
      ax.plot(life['x'], life['y'], linestyle='-', linewidth=2, color='lightpink')
      
      if data_type == 'population':
        ax.set_title(f'Liczebność populacji w pokoleniu {str(frame)}')
        ax.set_xlabel('Pokolenie')
        ax.set_ylabel('Populacja')
        
      elif data_type == 'fitness':
        ax.set_title(f'Średni fitness w pokoleniu {str(frame)}')
        ax.set_xlabel('Pokolenie')
        ax.set_ylabel('Fitness')
      ax.tick_params(axis='x')
      ax.set_ylim(0, 1.15 * max(values))
      ax.set_xlim(0, time)
  frames = range(time+1)
  animation = FuncAnimation(fig, update, frames=frames, interval=500)
  animation.save(os.path.join(subfolder_path, f'{data_type}.gif'), writer='pillow')
  fig.savefig(os.path.join(subfolder_path, f'{data_type}_final.jpg'))
