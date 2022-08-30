import ast
from vector import Vector
import math 


def distance(x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

def fill_borders(borders):
    with open("store.txt", 'r') as s:
        x = s.readline()
        res = ast.literal_eval(x)
        # Remove gaps
        for i, entry in enumerate(res):
            for j, sec in enumerate(res):
                if i != j:
                    if 0 < distance(entry[0], entry[1], sec[0], sec[1]) <= 15:
                        res[i] = res[j]
        for i in range(0, len(res), 2):
            borders.append(Vector(res[i][0], res[i][1],res[i+1][0], res[i+1][1]))

def read_borders(file, borders):
    with open(file, 'r') as s:
        x = s.readline()
        res = ast.literal_eval(x)
        for border in res:
            start, end = border
            borders.append(Vector(start[0], start[1], end[0], end[1]))
    
    

def get_checks(checks):
    with open("checks.txt", 'r') as s:
        x = s.readline()
        res = ast.literal_eval(x)
        for elem in res:
            checks.append(elem)

if __name__ == '__main__':
    b = []
    read_borders("borders.txt", b)
