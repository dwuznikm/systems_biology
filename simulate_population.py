import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os
import simulation_tools as st


#parser json -  parametru
# DEADLINE 16 KWIETNIA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
# próba komentarza

# Funkcja aktualizacji max_fitness na podstawie wielkości populacji
# porobić symulacje z różnym sd dla opt_genotypu i pop_genotypu
# ZROBIE PCA OBIECUJE


def simulate(N, n, time, opt_genotype_sd=1, pop_genotype_sd=0.5, mi=random.uniform(0.35, 1)):
  print(mi)
  # Create a folder to store the results
  current_time = datetime.now().strftime("%d.%m.%Y-%H-%M-%S")
  results_folder = 'results'
  subfolder_path = os.path.join(results_folder, current_time)
  os.makedirs(subfolder_path)

  max_fitness = st.calculate_max_fitness(N)
  optimal_genotype = st.random_genotype(n)
  genotype_df = pd.DataFrame(columns=[f'cecha{str(i)}' for i in range(n)])
  phenotype_df = pd.DataFrame(columns=['phenotype'])

  for i in range(N):
      genotype = st.random_genotype(n)
      genotype_df.loc[i] = genotype
      phenotype_df.loc[i] = st.fitness(optimal_genotype, genotype)

    # life loop

  population_size = {'x':[], 'y':[]}
  phenotypes = [phenotype_df.mean()]
  population_sizes = [phenotype_df.shape[0]]
  pca_df_list=[genotype_df.copy()]
  opt_df = pd.DataFrame(columns=[f'cecha{str(i)}' for i in range(n)])
  opt_df.loc[0] = optimal_genotype

  new_optimal_genotype = optimal_genotype
  for pokolenie in range(time):
    birth_list = []
    new_optimal_genotype = st.calculate_optimal_genotype(mi, new_optimal_genotype, opt_genotype_sd, n)
    for i in range(phenotype_df.shape[0]):
        if phenotype_df.iloc[i].phenotype < max_fitness:
          children_count = st.children_roullete(phenotype_df.iloc[i].phenotype, max_fitness)
          for child in range(children_count):
            new_genotype = []
            for j in range(genotype_df.shape[1]):
                new_value = st.mutation(mi, genotype_df.iloc[i, j], pop_genotype_sd)
                new_genotype.append(new_value)
            birth_list.append((new_genotype, st.fitness(new_optimal_genotype, new_genotype)))
    genotype_df.drop(genotype_df.index, inplace=True)
    phenotype_df.drop(phenotype_df.index, inplace=True)
    for i in range(len(birth_list)):
      genotype_df.loc[i] = birth_list[i][0]
      phenotype_df.loc[i] = birth_list[i][1]
    phenotypes.append(phenotype_df.mean())
    population_sizes.append(phenotype_df.shape[0])
    max_fitness = st.calculate_max_fitness(phenotype_df.shape[0])
    if genotype_df.shape[0] == 0:
      time = pokolenie
      break
    pca_df_list.append(genotype_df.copy())
    opt_df.loc[len(opt_df)]=new_optimal_genotype

    print(f'Pokolenie {pokolenie+1} AVG Fitness: {round(phenotype_df.mean().values[0], 2)}, max_fitness: {max_fitness} Population: {phenotype_df.shape[0]}')

  phenotypes_values = [series.values[0] for series in phenotypes]

  st.create_plot(phenotypes_values, time, subfolder_path, data_type='fitness')
  st.create_plot(population_sizes, time, subfolder_path, data_type='population')
  if n!=2:
    pca_pop_and_opt_gen = st.perform_pca(pca_df_list, opt_df)
    st.pca_scatter(pca_pop_and_opt_gen, time, subfolder_path)
  elif n==2:
    st.two_dim_scatter(pca_df_list, opt_df, time, subfolder_path)
  
  
  
  

N0=500
n=2
time=100
opt_genotype_sd=0.5
pop_genotype_sd=0.8

simulate(N0, n, time, opt_genotype_sd, pop_genotype_sd)
