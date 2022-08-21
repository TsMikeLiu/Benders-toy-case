from gurobipy import *
import numpy as np

# Constant Params
A = np.matrix([[1,0,0,1,0,0,0,0],
              [0,1,0,0,1,0,0,0],
              [0,0,1,0,0,1,0,0],
              [1,0,1,0,0,0,1,0],
              [1,1,0,0,0,0,0,1]])
C = np.array([1,1,1,1,1])
b = np.array([8,3,5])
B = np.array([8,3,5,5,3])

# Build Model
MP = Model()
SP = Model()

# add Variables
y = MP.addMVar(shape=5, obj=7, vtype=GRB.BINARY, name='y')
z = MP.addMVar(shape=1, obj=1, lb=0, vtype=GRB.CONTINUOUS, name='z')

lambda1 = SP.addMVar(shape=3, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name='lambda1')
lambda2 = SP.addMVar(shape=5, lb=-GRB.INFINITY, ub=0, vtype=GRB.CONTINUOUS, name='lambda2')

x = [] # to save the final value of x
SP_CONS = SP.addConstr(A.T[0:3,:].T @ lambda1 + A.T[3:8,:].T @ lambda2  <= C)
SP.Params.InfUnbdInfo = 1


MP.optimize()
iter = 0
SP_Dual_Obj = 10000

while SP_Dual_Obj>z.x:
    print("*****************************************")
    print("*****************************************")
    print("*************** ITERATION {0} *************".format(iter+1))
    print("*****************************************")
    print("*****************************************")
    print("*****************************************")
    # Solve Master Problem
    b1 = np.array(y.x) * B
    print(b1)
    SP.setObjective(b @ lambda1 + b1 @ lambda2, GRB.MAXIMIZE)
    SP.optimize()
        

    
    # add feasibily cut
    if SP.status == GRB.Status.UNBOUNDED:
        ray = np.array(SP.UnbdRay)
        print("Starting Adding Feasibily Cut")
        print(ray)
        print(b*ray[0:3])
        constant = np.sum(b*ray[0:3],axis=0)
        y_coef = B * ray[3:8]
        print(y_coef)
        MP.addConstr(constant + y_coef@y <= 0)
        print("Ending Adding Feasibily Cut")
    
    # add optimality cut 
    elif SP.status == GRB.Status.OPTIMAL:
        SP_Dual_Obj = SP.ObjVal
        x.append(SP_CONS.pi)
        print("Starting Adding Optimality Cut")
        dual1 = lambda1.x
        dual2 = lambda2.x
        print(dual1)
        print(dual2)
        constant = np.sum(b*dual1,axis=0)
        y_coef = B * dual2
        print(y_coef)
        MP.addConstr(constant + y_coef@y <= z)
        print("Ending Adding Optimality Cut")
        
    
    
    MP.optimize()
    iter += 1

print("Optimal Solution:")
print(y.x)
print(x)