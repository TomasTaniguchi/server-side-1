import random


def account():
    mapchapters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
    result = random.choices(mapchapters, k=4)
    code = ''
    for i in result:
        code += str(i)
    code = code
    return code

def entity():
    mapchapters = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    result = random.choices(mapchapters, k=4)
    code = ''
    for i in result:
        code += str(i)
    code = code
    return code

def code():
    mapchapters = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
    result = random.choices(mapchapters, k=4)
    code = ''
    for i in result:
        code += str(i)
    code = code
    return code

def area():
    mapchapters = ['1', 'W', '3', 'E', '5', 'R', '7', 'T', 'Y', '0']
    result = random.choices(mapchapters, k=4)
    code = ''
    for i in result:
        code += str(i)
    code = code
    return code

def white_space(text):
    map =[' ', '  ', '   ', '    ']
    result = random.choices(map, k=4)
    withe = ''
    for i in result:
        withe += str(i)
    text = text + withe
    return text