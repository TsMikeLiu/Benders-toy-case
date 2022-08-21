from gurobipy import *
import numpy as np

m = Model()
x = m.addMVar(shape=3, obj=2, lb=0, vtype=GRB.CONTINUOUS, name='x')
A = np.matrix([[1,0,0],
              [0,1,0],
              [0,0,1]])
B = np.array([1,2,3])
C = np.array([1,4,7])
# A = np.matrix([[1,1,1]])
A = np.array([1,3,1])
m.addConstr(A @ x >= 4, name='c')
# m.setObjective(B@x, GRB.MINIMIZE)
m.optimize()
# print(x[0].x)
# print(x[1].x)
# print(x[2].x)
print(x.x)

a0 = np.array([1,1,1,1,1])
a1 = np.array([8,3,5])
a2 = np.array([8,3,5,5,3])
print(a0*a2)

aa = np.matrix([1,2,3])
print(aa)