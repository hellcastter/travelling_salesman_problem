import random

result = ""

number = 200
for i in range(number):
    for j in range(number):
        if i == j:
            result += f"{i+1},{j+1},{0}\n"
            continue
        
        result += f"{i+1},{j+1},{random.randint(1, number)}\n"
        
result = result[:-1]
print('writing')    
with open('graph.csv', 'w', encoding='utf-8') as file:
    file.write(result)