import numpy as np
import re
import time
import random

import random

def gerar_populacao_gulosa(tamanho_populacao, n, value, weight, capacity):
    populacao = []

    def heuristica_gulosa():
        itens_selecionados = [0] * n 
        peso_total = 0
        valor_total = 0
        
        itens_ordenados = sorted(range(n), key=lambda i: value[i] / weight[i], reverse=True)

        for i in itens_ordenados:
            if peso_total + weight[i] <= capacity:
                itens_selecionados[i] = 1
                peso_total += weight[i]
                valor_total += value[i]

        return itens_selecionados, valor_total

    while len(populacao) < tamanho_populacao:
        individuo, valor_total = heuristica_gulosa()

        #solução válida
        if valor_total > 0:
            populacao.append(individuo)
    return populacao;

def mochila_genetic(n, value, weight, capacity, num_geracoes, tamanho_populacao, taxa_mutacao=0.1):
    # Fitness
    def calcular_fitness(individuo):
        peso_total = sum(peso * item for peso, item in zip(weight, individuo))
        valor_total = sum(valor * item for valor, item in zip(value, individuo))
        if peso_total > capacity:
            return 0  # Peso excedido
        return valor_total
    
    # Crossover
    def crossover(individuo1, individuo2):
        ponto_corte = random.randint(1, n - 1)
        filho1 = individuo1[:ponto_corte] + individuo2[ponto_corte:]
        filho2 = individuo2[:ponto_corte] + individuo1[ponto_corte:]
        return filho1, filho2

    # Mutação
    def mutacao(individuo, taxa_mutacao):
        for i in range(n):
            if random.random() < taxa_mutacao:
                individuo[i] = 1 - individuo[i]

    # População inicial gulosa
    populacao = gerar_populacao_gulosa(tamanho_populacao, n, value, weight, capacity)
    for geracao in range(num_geracoes):
        aptidoes = [calcular_fitness(individuo) for individuo in populacao]
        
        #Selecao de pais
        pais = random.choices(populacao, weights=aptidoes, k=tamanho_populacao)
        
        filhos = []
        for i in range(0, tamanho_populacao, 2):
            filho1, filho2 = crossover(pais[i], pais[i + 1])
            filhos.extend([filho1, filho2]) 
        
        # Mutação
        for individuo in filhos:
            mutacao(individuo, taxa_mutacao)
        
        # Nova população
        populacao = filhos

    melhor_individuo = max(populacao, key=calcular_fitness)
    melhor_valor = calcular_fitness(melhor_individuo)
    return melhor_valor, melhor_individuo

def solve_knapsack_problem(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    capacity = int(lines[-1].strip())
    
    id, value, weight = [], [], []
    for line in lines[1:-1]:
        numbers = re.findall(r"[0-9]+", line)
        id.append(int(numbers[0]) - 1)
        value.append(int(numbers[1]))
        weight.append(int(numbers[2]))
    max_value, melhor_individuo = mochila_genetic(n, value, weight, capacity, num_geracoes=10, tamanho_populacao=1000, taxa_mutacao=0.1)
    return max_value

def main():
    output_max_values = []

    for iterator in range(1, 5):
        input_file_path = f"input/input{iterator}.in"
        max_value = solve_knapsack_problem(input_file_path)
        output_max_values.append(max_value)
        output_line = f"Instancia {iterator} : {max_value}\n"
        
        with open("output/genetic.out", "a+") as output_file:
            output_file.write(output_line)

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    
    with open("output/genetic_execution_time.out", "a+") as output_file:
            output_file.write(str(execution_time))
            
    print(f"Execution time: {execution_time} seconds")
