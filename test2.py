import pulp as pulp
import numpy as np

# Define characters to include in the keyboard layout
characters = list('abcdefghijklmnopqrstuvwxyz')

# Define character frequency
frequency = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
             'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
             'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
             'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
             'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
             'z': 0.00074}

# Define initial position of each character in QWERTY layout
qwerty_position = {'a': (0, 0), 'b': (0, 1), 'c': (0, 2), 'd': (0, 3), 'e': (0, 4),
                   'f': (0, 5), 'g': (0, 6), 'h': (0, 7), 'i': (0, 8), 'j': (0, 9),
                   'k': (0, 10), 'l': (0, 11), 'm': (0, 12), 'n': (0, 13), 'o': (0, 14),
                   'p': (0, 15), 'q': (1, 0), 'r': (1, 3), 's': (1, 2), 't': (1, 4),
                   'u': (1, 8), 'v': (1, 1), 'w': (1, 5), 'x': (1, 2), 'y': (1, 7),
                   'z': (1, 1)}

# Define distance matrix
distance = np.zeros((len(characters), len(characters)))
for i in range(len(characters)):
    for j in range(len(characters)):
        xi, yi = qwerty_position[characters[i]]
        xj, yj = qwerty_position[characters[j]]
        distance[i, j] = np.sqrt((xi-xj)**2 + (yi-yj)**2)

# Define the optimization problem
problem = pulp.LpProblem('KeyboardLayoutOptimizer', pulp.LpMinimize)

# Define binary variables indicating if a character is assigned to a keyslot
assignment = pulp.LpVariable.dicts('Assignment', characters, cat='Binary')

# Define the objective function for performance
performance = pulp.lpSum(assignment[i] * assignment[j] * distance[i, j] / (frequency[i] + frequency[j])
                         for i in characters for j in characters)
problem += performance

# Define the objective function for ergonomics
ergonomics = pulp.lpSum(assignment[i] * assignment[j] * distance[i, j]**2 * (frequency[i] + frequency[j]))
                
problem += ergonomics
# Add constraint to ensure each character is assigned to exactly one keyslot

for i in characters:
    problem += pulp.lpSum(assignment[i]) == 1
#Add constraints to ensure each keyslot is assigned to at most one character

for i in range(len(qwerty_position)):
    problem += pulp.lpSum(assignment[c] for c in characters if qwerty_position[c] == (0, i)) <= 1
    problem += pulp.lpSum(assignment[c] for c in characters if qwerty_position[c] == (1, i)) <= 1
#Solve the optimization problem

problem.solve()
#Print the optimal keyboard layout

print('Optimal Keyboard Layout:')
for i in range(len(qwerty_position)):
    row = ''
    for j in range(len(qwerty_position[characters[0]])):
        c = [c for c in characters if pulp.value(assignment[c]) == 1 and qwerty_position[c] == (i, j)]
        row += c[0] if c else ' '
        print(row)
