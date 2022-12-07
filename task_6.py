def read(file_name):
    with open(file_name, 'r') as file:
        return file.read()


print(read('matrix.csv'))
