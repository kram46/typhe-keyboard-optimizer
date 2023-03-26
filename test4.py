import gurobipy as gp
import json

# Define the character set to be used on the keyboard
characters = "abcdefghijklmnopqrstuvwxyz"

# Define the keyslot set for the keyboard
keyslots = range(26)

# Define the frequency of each character in the character set
char_freq = {
    'a': 0.17410, 'b': 0.01836, 'c': 0.01836, 'd': 0.02648, 'e': 0.05567,
    'f': 0.01154, 'g': 0.06286, 'h': 0.02825, 'i': 0.07828, 'j': 0.00101,
    'k': 0.02790, 'l': 0.04132, 'm': 0.03661, 'n': 0.10147, 'o': 0.06298,
    'p': 0.02755, 'q': 0.00012, 'r': 0.03790, 's': 0.06074, 't': 0.05921,
    'u': 0.03119, 'v': 0.00530, 'w': 0.01024, 'x': 0.00129, 'y': 0.02025, 'z': 0.00094
}

# Define the time to type each pair of characters
with open('new_performance.json') as f:
    data = json.load(f)
new_data = {}
for key, value in data.items():
    new_key = tuple(key)
    new_data[new_key] = value
char_time = new_data

# Define the extreme movements of the wrist and fingers for each keyslot
ergo_score = {
    0: 2, 1: 2, 2: 2, 3: 2, 4: 2.5, 5: 3, 6: 2, 7: 2, 8: 2, 9: 2,
    10: 0, 11: 0, 12: 0, 13: 0, 14: 2, 15: 2, 16: 0, 17: 0, 18: 0, 
    19: 2, 20: 2, 21: 2, 22: 2, 23: 3.5, 24: 2, 25: 2
}

# Define the QWERTY positions for each character
# qwerty_pos = {
#     'a': 0, 'b': 13, 'c': 14, 'd': 3, 'e': 4,
#     'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
#     'k': 10, 'l': 11, 'm': 15, 'n': 12, 'o': 16,
#     'p': 17, 'q': 0, 'r': 2, 's': 3, 't': 5,
#     'u': 7, 'v': 12, 'w': 1, 'x': 14, 'y': 8, 'z': 13
# }

qwerty_pos = {
    'a': 10, 'b': 23, 'c': 21, 'd': 12, 'e': 2,
    'f': 13, 'g': 14, 'h': 15, 'i': 7, 'j': 16,
    'k': 17, 'l': 18, 'm': 25, 'n': 24, 'o': 8,
    'p': 9, 'q': 0, 'r': 3, 's': 11, 't': 4,
    'u': 6, 'v': 22, 'w': 1, 'x': 20, 'y': 5, 'z': 19
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

w_performance = 0.6
w_ergonomics = 0.2
w_familiarity = 0.2


m.setObjective(performance * w_performance + w_ergonomics * ergonomics + w_familiarity * familiarity, gp.GRB.MINIMIZE)

for i in characters:
    m.addConstr(gp.quicksum(char_slot[(i, k)] for k in keyslots) == 1, f"Assign {i}")

for k in keyslots:
    m.addConstr(gp.quicksum(char_slot[(i, k)] for i in characters) <= 1, f"Key slot {k} is assigned to at most one character")
# Solve the problem using Gurobi's default solver
m.optimize()

# Print the status of the problem (should be 'Optimal')
#print("Status:", gp.GRB.status[m.status])

# Print the optimal keyboard layout
print("Optimal Keyboard Layout:")
for k in keyslots:
    row = ""
    for i in characters:
        if char_slot[(i, k)].x == 1:
            row += i
    print(row)



