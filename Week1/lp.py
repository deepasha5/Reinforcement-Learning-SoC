import numpy as np
from pulp import *

#read data from input file 
with open('mdp2.txt') as f:
  
    states= int(f.readline().split(" ")[1])
    actions =int(f.readline().split(" ")[1])
    gamma =0

    data =[[[[0 for k in range(2)] for m in range(actions)]for j in range(states)] for i in range(states)]
    line ="empty"
    while line:
        line =f.readline()
        if (line.split(" ")[0]=="gamma"):
            gamma = float(line.split(" ")[2])
           
            break
        s1 = int(line.split(" ")[1])
        a = int(line.split(" ")[2])
        s2 =int(line.split(" ")[3])
        r = float(line.split(" ")[4])
        p = float(line.split(" ")[5])

        data[s1][s2][a][0]= r
        data[s1][s2][a][1]= p

pie = np.zeros(states)
problem = LpProblem('mdp', LpMinimize)
v_vars = LpVariable.dicts("V", [(i) for i in range (states)] , lowBound=0, cat='Continuous')


#Objective Function

problem += lpSum(v_vars[(i)] for i in range (states)) , 'Objective Function'

#Constraints
for a in range(actions):
    for i in range(states):
        problem += lpSum([data[i][s_next][a][1]*(data[i][s_next][a][0] +gamma * v_vars[(s_next)]) for s_next in range(states)]) <= v_vars[(i)]

problem.solve()

for i in range(states):
    optimal_v = 100000
    for a in range(actions):
        x =v_vars[(i)].varValue- sum([data[i][s_next][a][1]*(data[i][s_next][a][0] +gamma * v_vars[(s_next)].varValue) for s_next in range(states)]) 
        if (x < optimal_v):
            pie[i]=a
        optimal_v = min(optimal_v, x)
        

file1 = open("out.txt", "w")  # write mode
for i in range(states):
    file1.write(str(v_vars[(i)].varValue))
    file1.write(" ")
    file1.write(str(pie[i]))
    file1.write("\n")
# file1.write("policy :")
# file1.write(str(pie))
file1.close()
