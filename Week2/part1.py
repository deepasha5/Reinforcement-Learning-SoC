import subprocess
import numpy as np
import os




class MDP:
    def __init__(self) -> None:
        #self.N_s= subprocess.call(["/home/deepasha/Documents/soc+wids/week2/MDP" , "states"])
        p = subprocess.Popen(["/home/deepasha/Documents/soc+wids/week2/MDP", "states"],stdout=subprocess.PIPE, stdin=subprocess.PIPE, text =True)
        self.N_s= int(p.stdout.readline())
        p = subprocess.Popen(["/home/deepasha/Documents/soc+wids/week2/MDP", "actions"],stdout=subprocess.PIPE, stdin=subprocess.PIPE, text =True)
        self.N_a= int(p.stdout.readline())
        p = subprocess.Popen(["/home/deepasha/Documents/soc+wids/week2/MDP", "gamma"],stdout=subprocess.PIPE, stdin=subprocess.PIPE, text =True)
        self.gamma= float(p.stdout.readline().split("\n")[0])
        
        
        


class MonteCarloES:
    '''
    Implement your algorithm here, and define appropriate helper classes as required.
    Have a look at the sample solution for Week 1 that was uploaded to know the expected code structure.
    '''
    def __init__(self) -> None:
        self._MDP = MDP()
        self._policy = np.random.choice(self._MDP.N_a, self._MDP.N_s)
        self._value = np.random.rand(self._MDP.N_s, self._MDP.N_a)
        self._returns = np.zeros((self._MDP.N_s, self._MDP.N_a) , np.float64)
        self._freq = np.zeros((self._MDP.N_s, self._MDP.N_a) , np.float64)


    def _algo(self) -> np.float64:
        

        state = np.random.choice(self._MDP.N_s)
        action = np.random.choice(self._MDP.N_a)
        #generating episode 

        visited = np.zeros((self._MDP.N_s, self._MDP.N_a) , np.float64)
        
        nextstate= 3
        lis= []
        #lis.append(str(p.stdin.write(str(action)+'\n')))
        lis.append(action)
        


        for i in range(10):
            p = subprocess.Popen(["/home/deepasha/Documents/soc+wids/week2/MDP", "1"],stdout=subprocess.PIPE, stdin=subprocess.PIPE, text =True)
            
            for k in lis:
                os.system(str(p.stdin.write(str(k)+'\n')))

            p.stdin.close()
            stdout1= p.stdout.read()
           

            return_val = stdout1.split("\n")[nextstate+1].split(": ")[1]
            
            if (visited[state][action]==0) :
                visited[state][action] =1
                self._freq[state][action] =self._freq[state][action]  +1
                self._returns[state][action]= self._returns[state][action]+ float(return_val)
                self._value[state][action] = self._returns[state][action]/ self._freq[state][action]

            state= int(stdout1.split("\n")[nextstate].split(": ")[1])
            action = self._policy[int(state)]
            nextstate = nextstate+3
            lis.append(action)

        max_val =0

        for i in range(self._MDP.N_s):
            max_val =0
            for j in range(self._MDP.N_a):
                if (self._value[i][j]> max_val):
                    max_val =self._value[i][j]
                    self._policy[i]= j

    def solve(self) -> tuple:
        itr =100000
        for i in range (1000):
            self._algo()
            print(i)
        return self._value, self._policy

ins = MonteCarloES()
print(ins.solve())
