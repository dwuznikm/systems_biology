import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os

#parser json -  parametru
# DEADLINE 9 KWIETNIA!!!

results_folder = 'results'

def random_genotype(n):
  return [random.uniform(-10, 10) for i in range(n)]


# liczenie odległości między optymalnym fenotypem a naszym (ewentualnie do testowania inne warianty)
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


def calculate_optimal_genotype(mi, genotype, strenght):
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

# Funkcja aktualizacji max_fitness na podstawie wielkości populacji
# porobić symulacje z różnym sd dla opt_genotypu i pop_genotypu
# pca

def simulate(N, n, time, opt_genotype_sd=1, pop_genotype_sd=0.5, mi=np.random.random()):
  # Tworzymy subfolder z wynikami tej symulacji
  current_time = datetime.now().strftime("%d.%m.%Y-%H-%M-%S")
  subfolder_path = os.path.join(results_folder, current_time)
  os.makedirs(subfolder_path)

  max_fitness = calculate_max_fitness(N)
  optimal_genotype = random_genotype(n)
  genotype_df = pd.DataFrame(columns=[f'cecha{str(i)}' for i in range(n)])
  phenotype_df = pd.DataFrame(columns=['phenotype'])

  for i in range(N):
      genotype = random_genotype(n)
      genotype_df.loc[i] = genotype
      phenotype_df.loc[i] = fitness(optimal_genotype, genotype)

  #pętla 'życia' osobnika

  fig, ax = plt.subplots(figsize=(10, 7))
  fig2, ax2 = plt.subplots(figsize=(10, 7))

  life = {'x':[], 'y':[]}
  population_size = {'x':[], 'y':[]}
  phenotypes = [phenotype_df.mean()]
  population_sizes = [phenotype_df.shape[0]]
  for pokolenie in range(time):

      birth_list = []
      new_optimal_genotype = calculate_optimal_genotype(mi, optimal_genotype, opt_genotype_sd)
      for i in range(phenotype_df.shape[0]):
          if phenotype_df.iloc[i].phenotype < max_fitness:
            children_count = children_roullete(phenotype_df.iloc[i].phenotype, max_fitness)
            for child in range(children_count):
              new_genotype = []
              for j in range(genotype_df.shape[1]):
                  new_value = mutation(mi, genotype_df.iloc[i, j], pop_genotype_sd)
                  new_genotype.append(new_value)
              birth_list.append((new_genotype, fitness(new_optimal_genotype, new_genotype)))
      genotype_df.drop(genotype_df.index, inplace=True)
      phenotype_df.drop(phenotype_df.index, inplace=True)
      for i in range(len(birth_list)):
        genotype_df.loc[i] = birth_list[i][0]
        phenotype_df.loc[i] = birth_list[i][1]
      phenotypes.append(phenotype_df.mean())
      population_sizes.append(phenotype_df.shape[0])
      max_fitness = calculate_max_fitness(phenotype_df.shape[0])


      print(f'Pokolenie {pokolenie+1} AVG Fitness: {round(phenotype_df.mean().values[0], 2)}, max_fitness: {max_fitness} Population: {phenotype_df.shape[0]}')

  phenotypes_values = [series.values[0] for series in phenotypes]
  def update(frame):
      ax.clear()
      life['x'].append(frame)
      life['y'].append(phenotypes_values[frame])
      ax.plot(life['x'], life['y'], linestyle='-', linewidth=2, color='lightpink')
      ax.set_title(f'Średnie fenotypów(fitness) w pokoleniu {str(frame)}')
      ax.set_xlabel('Pokolenie')
      ax.set_ylabel('Fenotyp')
      ax.tick_params(axis='x')

      #Fixed axis
      ax.set_ylim(0, max(phenotypes_values) + 2)
      ax.set_xlim(0, time+1)

  def update2(frame):
      ax2.clear()
      population_size['x'].append(frame)
      population_size['y'].append(population_sizes[frame])
      ax2.plot(population_size['x'], population_size['y'], linestyle='-', linewidth=2, color='violet')
      ax2.set_title(f'Liczebność populacji w pokoleniu {str(frame)}')
      ax2.set_xlabel('Pokolenie')
      ax2.set_ylabel('Populacja')
      ax2.tick_params(axis='x')

      #Fixed axis
      ax2.set_ylim(min(population_sizes), 1.1 * max(population_sizes))
      ax2.set_xlim(0, time+1)

  frames = range(time+1)
  ani = FuncAnimation(fig, update, frames=frames, interval=500)
  population_change = FuncAnimation(fig2, update2, frames=frames, interval=500)

  ani.save(os.path.join(subfolder_path, f'phenotypes_{N}_{n}_{time}_{opt_genotype_sd}_{pop_genotype_sd}_{mi}.gif'), writer='pillow')
  population_change.save(os.path.join(subfolder_path, f'population_size_{N}_{n}_{time}_{opt_genotype_sd}_{pop_genotype_sd}_{mi}.gif'), writer='pillow')
  fig.savefig(os.path.join(subfolder_path, f'phenotypes_final_{N}_{n}_{time}_{opt_genotype_sd}_{pop_genotype_sd}_{mi}.jpg'))
  fig2.savefig(os.path.join(subfolder_path, f'population_size_final_{N}_{n}_{time}_{opt_genotype_sd}_{pop_genotype_sd}_{mi}.jpg'))


N0=500
n=5
time=10
opt_genotype_sd=0.5
pop_genotype_sd=0.5

simulate(N0, n, time, opt_genotype_sd, pop_genotype_sd)