import numpy as np

#read data from input file 
with open('mdp1.txt') as f:
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
     
        
 
max_iterations = 10000 
delta =  1e-5
np.random.seed(1) #so that results can be regenerated 

V = np.zeros(states) #value function (basically V_t)
pie = np.zeros(states) # optimal action to take from each state for max reward 

for i in range(max_iterations):
    max_delta = 0
    V_next= np.zeros(states) #(basically V_(t+1))

    for s in range(states): # iterating over all the states 
        max_val=0

        for a in range(actions) : #finding the action which gives the max reward 
            val =0
            for s_next in range(states):
                val = val + data[s][s_next][a][1]*(data[s][s_next][a][0] +gamma * V[s_next])

            max_val= max(max_val , val)

            if (V[s]< val):
                pie[s]= a  #best action stored here 

        V_next[s] = max_val

        max_delta = max(max_delta, abs(V[s]- V_next[s]))  #convergence condition

    V = V_next

    if max_delta< delta:
        break

file1 = open("out.txt", "w")  # write mode
file1.write("V :")
file1.write(str(V))
file1.write("\n")
file1.write("policy :")
file1.write(str(pie))
file1.close()
  

















