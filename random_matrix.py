""" generate random matrix """
import random

result = ""
number = 8

for i in range(number):
    for j in range(i, number):
        if i == j:
            result += f"{i+1},{j+1},{0}\n"
            continue

        if random.random() < .3:
            continue

        weight = random.randint(1, number)
        result += f"{i+1},{j+1},{weight}\n"

result = result[:-1]

print('writing')
with open('graph.csv', 'w', encoding='utf-8') as file:
    file.write(result)
