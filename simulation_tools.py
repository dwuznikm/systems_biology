import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os

from sklearn import datasets, decomposition
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def random_genotype(n):
  return [random.uniform(-10, 10) for i in range(n)]


def fitness(optimal_genotype, genotype):
    if len(optimal_genotype) != len(genotype):
        raise ValueError("Długość wektorów musi być taka sama.")
    suma_kwadratow_roznicy = sum((a - b)**2 for a, b in zip(optimal_genotype, genotype))
    fitness_value = math.sqrt(suma_kwadratow_roznicy)
    fitness_value /= len(optimal_genotype)

    return fitness_value


def mutation(mi, genotype, strenght):
  if random.random() < mi:
    p = np.random.normal(loc=0, scale=strenght)
    genotype += p
  return genotype


def calculate_optimal_genotype(mi, genotype, strenght, n, speed):
  if random.random() < mi:
    p = np.random.normal(loc=speed, scale=strenght, size=n)
    genotype += p
  return genotype

def meteor(mi, genotype, strenght, n, speed, meteor_chance):
  if random.random() > meteor_chance:
    return calculate_optimal_genotype(mi, genotype, strenght, n, speed), 'NoMeteor'
  else:
    print('meteor')
    return calculate_optimal_genotype(1, genotype, strenght*3, n, speed*12), 'Meteor'

def children_roullete(fitness, max_fitness):
  exponent = (max_fitness - fitness)/15
  l = np.exp(exponent)
  children_amount = np.random.poisson(lam=l)
  return min(8, children_amount)

def calculate_max_fitness(population, n, mode):
  if mode == 'Limited resources':
    return min(max(700*(2/3*n)/population, 1), 13)/n
  elif mode == 'Standard':
    return min(max(1800*(2/3*n)/population, 2), 14)/n
  elif mode == 'Many resources':
    return min(max(2500*(2/3*n)/population, 3), 15)/n


def create_plot(values, time, subfolder_path, data_type):
  if time!=0:
    life = {'x':[], 'y':[]}
    fig, ax = plt.subplots(figsize=(10, 7))
    print(values)
    
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


def perform_pca(population_list, optimal_genotype_df):
  pca_list = []
  for time_step, (population_df, optimal_genotype_row) in enumerate(zip(population_list, optimal_genotype_df.iterrows())):
    population_array = population_df.values    
    optimal_genotype = optimal_genotype_row[1].values.reshape(1, -1)
    data = np.vstack((population_array, optimal_genotype))
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data)
    pca_df = pd.DataFrame(data=pca_result, columns=['PCA1', 'PCA2'])
    pca_list.append(pca_df)
  print(len(pca_list))
  return pca_list

def two_dim_scatter(df_list, opt_df, population_sizes, time, subfolder_path, meteorlist):
  if time!=0:
    fig, ax = plt.subplots(figsize=(10, 7))
    max_x = 0
    max_y = 0
    min_x = 0
    min_y= 0
    for df in df_list:
      maximum_x = df["cecha0"].max()
      maximum_y = df["cecha1"].max()
      if maximum_x > max_x:
        max_x = maximum_x
      if maximum_y > max_y:
        max_y = maximum_y
    if opt_df["cecha0"].max() > max_x:
      max_x = opt_df["cecha0"].max()
    if opt_df["cecha1"].max() > max_y:
      max_y = opt_df["cecha1"].max()

    for df in df_list:
      minimum_x = df["cecha0"].min()
      minimum_y = df["cecha1"].min()
      if minimum_x < min_x:
        min_x = minimum_x
      if minimum_y < min_y:
        min_y = minimum_y

    if opt_df["cecha0"].min() < min_x:
      min_x = opt_df["cecha0"].min()
    if opt_df["cecha1"].min() < min_y:
      min_y = opt_df["cecha1"].min()

    def update(frame):
        ax.clear()
        ax.scatter(df_list[frame]['cecha0'], df_list[frame]['cecha1'], color='blue', label='Population', alpha=0.5)
        ax.scatter(opt_df['cecha0'].iloc[frame], opt_df['cecha1'].iloc[frame], color='red', marker='s', s=100, label='Optimal Genotype')
        ax.set_title(f'Genotypy osobników w pokoleniu {str(frame)}')
        #ax.set_xlabel(f'Population size: {population_sizes[frame]}')
        ax.text(0.5, -0.1, f'Population size: {population_sizes[frame]}', ha='center', transform=ax.transAxes)
        ax.tick_params(axis='x')
        ax.set_ylim(1.15*min_y, 1.15 * max_y)
        ax.set_xlim(1.15*min_x, 1.15 * max_x)
        if meteorlist[frame-1] == "Meteor":
          ax.text(0.5, 0.9, "Meteor", color='r', horizontalalignment='center', verticalalignment='top', transform=ax.transAxes)

    frames = range(time+1)
    animation = FuncAnimation(fig, update, frames=frames, interval=500)
    animation.save(os.path.join(subfolder_path, f'2d.gif'), writer='pillow')

def pca_scatter(df_list, time, population_sizes, subfolder_path, meteorlist):
  if time!=0:
    fig, ax = plt.subplots(figsize=(10, 7))
    max_x = 0
    max_y = 0
    min_x = 0
    min_y= 0
    for pca_df in df_list:
      maximum_x = pca_df["PCA1"].max()
      maximum_y = pca_df["PCA2"].max()
      if maximum_x > max_x:
        max_x = maximum_x
      if maximum_y > max_y:
        max_y = maximum_y

    for pca_df in df_list:
      minimum_x = pca_df["PCA1"].min()
      minimum_y = pca_df["PCA2"].min()
      if minimum_x < min_x:
        min_x = minimum_x
      if minimum_y < min_y:
        min_y = minimum_y

    def update(frame):
        ax.clear()
        ax.scatter(df_list[frame]['PCA1'][:-1], df_list[frame]['PCA2'][:-1], color='blue', label='Population', alpha=0.5)
        ax.scatter(df_list[frame].iloc[-1]['PCA1'], df_list[frame].iloc[-1]['PCA2'], color='red', marker='s', s=100, label='Optimal Genotype')
        ax.tick_params(axis='x')
        ax.set_title(f'Genotypy osobników w pokoleniu {str(frame)}')
        #fix placement
        ax.text(0.5, -0.1, f'Population size: {population_sizes[frame]}', ha='center', transform=ax.transAxes)
        #ax.set_xlabel(f'Population size: {population_sizes[frame]}')
        ax.set_ylim(1.15*min_y, 1.15 * max_y)
        ax.set_xlim(1.15*min_x, 1.15 * max_x)
        if meteorlist[frame-1] == "Meteor":
          ax.text(0.5, 0.9, "Meteor", color='r', horizontalalignment='center', verticalalignment='top', transform=ax.transAxes)

        
      
    frames = range(time+1)
    animation = FuncAnimation(fig, update, frames=frames, interval=500)
    animation.save(os.path.join(subfolder_path, f'2d.gif'), writer='pillow')