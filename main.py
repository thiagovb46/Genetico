import numpy as np
import re
import time
import random

count_itens = 0;  # Número de itens disponíveis
id = []
weight = []
value = [] 
capacity = 0 ;


def find_fitness(individuo):
    global capacity;
    global weight;
    global value;
    peso_total = 0
    valor_total = 0

    for i in range(len(individuo)):
        if individuo[i] == 1:  # Verifica se o item está na mochila
            peso_total += weight[i]
            valor_total += value[i]

    # Penalize soluções inválidas (se o peso total exceder a capacidade da mochila)
    if peso_total > capacity:
        return 0
    return valor_total

#Solucao e valor máximo obtido
def genetic_solution():
    best_solution = []
    best_value = 0
    # Defina os parâmetros do algoritmo genético
    tamanho_populacao = 100
    taxa_mutacao = 0.1
    num_geracoes = 1
    # Inicialize a população com indivíduos aleatórios  
    populacao = [[random.randint(0, 1) for _ in range(len(value))] for _ in range(tamanho_populacao)]
    for geracao in range(num_geracoes):
    # Avalie o fitness de cada indivíduo
        aptidoes = [find_fitness(individuo) for individuo in populacao]
        #Seleciona os pais mais aptos
        pais = random.choices(populacao, weights=aptidoes, k=tamanho_populacao)
        filhos = []
    #Crossover de um ponto
    global count_itens;
    for i in range(0, tamanho_populacao, 2):
        pai1, pai2 = pais[i], pais[i + 1]
        ponto_corte = random.randint(1, count_itens - 1)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        filhos.extend([filho1, filho2])
    #Mutação
    for individuo in filhos:
        for i in range(count_itens):
            if random.random() < taxa_mutacao:
                individuo[i] = 1 - individuo[i]
    populacao = filhos;

    best_solution = max(populacao, key =  find_fitness)
    best_value = find_fitness(best_solution);

    return best_solution, best_value

def solve_knapsack_problem(file_path):
    global count_itens;
    global capacity;
    with open(file_path, "r") as file:
        lines = file.readlines()
    count_itens = int(lines[0].strip())
    print(int(lines[-1].strip()))
    capacity = int(lines[-1].strip())
    print(capacity)
    
    for line in lines[1:-1]:
        numbers = re.findall(r"[0-9]+", line)
        id.append(int(numbers[0]) - 1)
        value.append(int(numbers[1]))
        weight.append(int(numbers[2]))
    #return n, value, weight, capacity

def main():
    output_max_values = []

    for iterator in range(1, 5):
        input_file_path = f"input/input{iterator}.in"
        solve_knapsack_problem(input_file_path)
        solution, max_value = genetic_solution()
        output_max_values.append(max_value)
        output_line = f"Instancia {iterator} : {max_value}\n"
        
        with open("output/genetic.out", "a+") as output_file:
            output_file.write(output_line)

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")