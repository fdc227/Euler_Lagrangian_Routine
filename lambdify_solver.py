from sympy import *
import pickle
import numpy
from numpy.linalg import inv
from scipy.integrate import odeint

A_raw = open('A.pkl', 'rb')
A = pickle.load(A_raw)
b_raw = open('b.pkl', 'rb')
b = pickle.load(b_raw)

IC_raw = open('IC.pkl', 'rb')
IC = pickle.load(IC_raw)
q_IC, parameter_IC = IC[0], IC[1]

############################################
######## STANDARD VARIABLE GEN FORM ########
############################################

var_raw = open('variable_list_str.pkl', 'rb')
variable_list_str = pickle.load(var_raw)
var_list_str, parameter_list_str = variable_list_str[0], variable_list_str[1]

parameter_list = []
for i in parameter_list_str:
    globals()[i] = symbols(i)

var_list = []
for i in var_list_str:
    j = i[0:-3]
    globals()[j] = symbols(j)
    var_list.append(globals()[j])
var_list_dt = []
for i in var_list_str:
    j = i[0:-3] +'_dt'
    globals()[j] = symbols(j)
    var_list_dt.append(globals()[j])
var_list_dt_dt = []
for i in var_list_str:
    j = i[0:-3] +'_dt_dt'
    globals()[j] = symbols(j)
    var_list_dt_dt.append(globals()[j])

#############################################
##################  END  ####################
#############################################

A_f = lambdify([*var_list, *var_list_dt], A, 'numpy')
b_f = lambdify([*var_list, *var_list_dt], b, 'numpy')

def EL(y, t, ):
    return (-1) * numpy.dot(inv(A_f), b_f) 

t = numpy.linspace(0, 10, 101)
sol = odeint(EL, q_IC, t)

