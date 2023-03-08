import gurobipy as gp

# Define the character set to be used on the keyboard
characters = "abcdefghijklmnopqrstuvwxyz"

# Define the keyslot set for the keyboard
keyslots = range(26)

# Define the frequency of each character in the character set
char_freq = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974, 'z': 0.00074
}

# Define the time to type each pair of characters
char_time = {(i, j):0 for i in characters for j in characters}

# Define the extreme movements of the wrist and fingers for each keyslot
ergo_score = {
    0: 10, 1: 7, 2: 7, 3: 4, 4: 4,
    5: 4, 6: 2, 7: 2, 8: 2, 9: 0,
    10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
    15: 0, 16: 0, 17: 0, 18: 2, 19: 2,
    20: 2, 21: 4, 22: 4, 23: 4, 24: 7,
    25: 7, 26: 7, 27: 10, 28: 10, 29: 10
}

# Define the QWERTY positions for each character
qwerty_pos = {
    'a': 0, 'b': 13, 'c': 14, 'd': 3, 'e': 4,
    'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 15, 'n': 12, 'o': 16,
    'p': 17, 'q': 0, 'r': 2, 's': 3, 't': 5,
    'u': 7, 'v': 12, 'w': 1, 'x': 14, 'y': 8, 'z': 13
}

# Create the Gurobi optimization model
m = gp.Model("KeyboardLayoutOptimizer")

# Define the decision variables, which are binary variables indicating whether a character is assigned to a keyslot
char_slot = m.addVars(characters, keyslots, vtype=gp.GRB.BINARY, name="char_slot")

# Define the performance objective function
performance = gp.quicksum(char_time[i,j] * char_slot[i,k] * char_slot[j,l] for i in characters for j in characters for k in keyslots for l in keyslots)

# Define the ergonomics objective function
ergonomics = gp.quicksum(char_freq[i] * ergo_score[k] * char_slot[i,k] for i in characters for k in keyslots)

# Define the familiarity objective function
familiarity = gp.quicksum(char_freq[i] * abs(qwerty_pos[i]-k) * char_slot[i,k] for i in characters for k in keyslots)

w_performance = 1
w_ergonomics = 0.1
w_familiarity = 0.1

m.setObjective(performance - w_ergonomics * ergonomics - w_familiarity * familiarity, gp.GRB.MAXIMIZE)

for i in characters:
    m.addConstr(gp.quicksum(char_slot[(i, k)] for k in keyslots) == 1, f"Assign {i}")

# Solve the problem using Gurobi's default solver
m.optimize()

# Print the status of the problem (should be 'Optimal')
print("Status:", gp.GRB.status[m.status])

# Print the optimal keyboard layout
print("Optimal Keyboard Layout:")
for k in keyslots:
    row = ""
    for i in characters:
        if char_slot[(i, k)].x == 1:
            row += i
    print(row)


