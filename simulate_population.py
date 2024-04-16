import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os
import simulation_tools as st



def simulate(N, n, time, opt_genotype_sd, pop_genotype_sd, speed, resources, mi=random.uniform(0.35, 1), meteor_chance=0):
  current_time = datetime.now().strftime("%d.%m.%Y-%H-%M-%S")
  results_folder = 'results'
  subfolder_path = os.path.join(results_folder, current_time)
  os.makedirs(subfolder_path)

  max_fitness = st.calculate_max_fitness(N, n, resources)
  optimal_genotype = st.random_genotype(n)
  genotype_df = pd.DataFrame(columns=[f'cecha{str(i)}' for i in range(n)])
  phenotype_df = pd.DataFrame(columns=['phenotype'])

  for i in range(N):
      genotype = st.random_genotype(n)
      genotype_df.loc[i] = genotype
      phenotype_df.loc[i] = st.fitness(optimal_genotype, genotype)

  population_size = {'x':[], 'y':[]}
  phenotypes = [phenotype_df.mean()]
  population_sizes = [phenotype_df.shape[0]]
  pca_df_list=[genotype_df.copy()]
  opt_df = pd.DataFrame(columns=[f'cecha{str(i)}' for i in range(n)])
  opt_df.loc[0] = optimal_genotype
  meteor_list = []
  new_optimal_genotype = optimal_genotype
  for pokolenie in range(time):
    birth_list = []
    
    new_optimal_genotype, if_meteor = st.meteor(mi, new_optimal_genotype, opt_genotype_sd, n, speed, meteor_chance)
    meteor_list.append(if_meteor)
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
    if genotype_df.shape[0] == 0:
      time = pokolenie
      break
    max_fitness = st.calculate_max_fitness(phenotype_df.shape[0], n, resources)
    pca_df_list.append(genotype_df.copy())
    opt_df.loc[len(opt_df)]=new_optimal_genotype

    print(f'Pokolenie {pokolenie+1} AVG Fitness: {round(phenotype_df.mean().values[0], 2)}, max_fitness: {max_fitness} Population: {phenotype_df.shape[0]}')

  phenotypes_values = [series.values[0] for series in phenotypes]

  st.create_plot(phenotypes_values, time, subfolder_path, data_type='fitness')
  st.create_plot(population_sizes, time, subfolder_path, data_type='population')
  if n!=2:
    pca_pop_and_opt_gen = st.perform_pca(pca_df_list, opt_df)
    st.pca_scatter(pca_pop_and_opt_gen, population_sizes, time, subfolder_path)
  elif n==2:
    st.two_dim_scatter(pca_df_list, opt_df, population_sizes, time, subfolder_path, meteor_list)
  return subfolder_path
  
import streamlit as stream



# Parametry symulacji

N0 = stream.number_input("Początkowa liczba osobników (N)", min_value=100, max_value=1000, value=500, step=10)
n = stream.number_input("Liczba cech genetycznych (n)", min_value=1, max_value=10, value=2, step=1)
time = stream.number_input("Liczba pokoleń (time)", min_value=10, max_value=200, value=100, step=10)
opt_genotype_sd = stream.number_input("Odchylenie standardowe dla genotypu optymalnego", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
pop_genotype_sd = stream.number_input("Odchylenie standardowe dla genotypu populacji", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
speed = stream.number_input("Prędkość mutacji (speed)", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
resources = stream.selectbox("Poziom zasobów", ["Many resources", "Standard", "Limited resources"])
mi = stream.slider("Współczynnik mutacji (mi)", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
meteor_chance = stream.slider("Szansa na wystąpienie zjawiska meteoru", min_value=0.0, max_value=1.0, value=0.5, step=0.01)



# Definicja funkcji symulacji w aplikacji Streamlit
def simulate_streamlit(N, n, time, opt_genotype_sd, pop_genotype_sd, speed, resources, mi, meteor_chance):
    stream.write("Symulacja rozpoczęta...")
    stream.write(f"Parametry symulacji: N={N}, n={n}, time={time}, opt_genotype_sd={opt_genotype_sd}, pop_genotype_sd={pop_genotype_sd}, speed={speed}, resources={resources}, mi={mi}, meteor_chance={meteor_chance}")

      # Wywołanie istniejącej funkcji symulacji
    actual_path=simulate(N, n, time, opt_genotype_sd, pop_genotype_sd, speed, resources, mi, meteor_chance)

    stream.write("Symulacja zakończona. Wyniki zapisane w folderze 'results'.")
    return actual_path



# Funkcja do ładowania wykresów z podfolderów w folderze wynikowym
def load_plots_from_folders(results_folder_path):
    plots = []
    # for date_folder in os.listdir(results_folder_path):
    #     date_folder_path = os.path.join(results_folder_path, date_folder)
    if os.path.isdir(results_folder_path):
        for file_name in os.listdir(results_folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".gif"):
                file_path = os.path.join(results_folder_path, file_name)
                plots.append(file_path)
    return plots

# Tworzenie interfejsu użytkownika za pomocą Streamlit
stream.title("Symulator populacji")

# Przycisk uruchamiający symulację
if stream.button("Uruchom symulację"):
    actual_path=simulate_streamlit(N0, n, time, opt_genotype_sd, pop_genotype_sd, speed, resources, mi, meteor_chance)
    print(actual_path)

    # Ładowanie wykresów z podfolderów w folderze wynikowym
    plots = load_plots_from_folders(actual_path)
    stream.markdown("### Wykresy:")
    for plot in plots:
      stream.image(plot, caption=os.path.basename(plot), use_column_width=True)
