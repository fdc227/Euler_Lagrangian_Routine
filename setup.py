from sympy import *
import pickle
from shape_gen import shape_gen



###############################################
###########     USER DEFINITION      ##########
###############################################

##### Put variables as a list of strings ######

var_list_str = []
parameter_list_str = ['L', 'E', 'I', 'rho', 'A']

########## DEFINE VARIABLE STRINGS ############

q_list = []
q_list_dot = []
for i in range(1, 11):
    q_list.append(f'q{i}(t)')
    q_list_dot.append(f'q{i}_dot(t)')

var_list_str = [*q_list, *q_list_dot]

############ Initial Conditions  ##############

IC = []
# Assuming r = 10cm = 0.1m
parameter_IC = [1, 10**6, 0.75*10**(-4), 2.7*10**3, 3.14*10**(-2)]
q_IC = []
for i in range(10):
    q_IC.append((i+1)*0.2)
for i in range(10):
    q_IC.append(0.2)

IC = [q_IC, parameter_IC]

###############################################

##### Express the kinetic and potential energy in terms of strings in sympy form #####
##### If expressions appear in terms of repeating patterns, write one single expression and a list of variables upon which the pattern will be applied ######
##### use 'diff(q, t)' to express the first order derivative of variable 'q' #####

x, y = symbols('x, y')
L = symbols('L')
shapes = shape_gen(4)
beam_shapes = []
for term in shapes:
    new_term = term.xreplace({x:y})
    beam_shapes.append(new_term)
print(beam_shapes)

k1, k2, k3, k4 = symbols('k1, k2, k3, k4') # Symbols for positional-identification

f = beam_shapes[0]*k1 + beam_shapes[1]*k2 + beam_shapes[2]*k3 + beam_shapes[3]*k4
T_func_f_format = f'integrate(1/2*rho*A*Derivative({f},t)**2, (y, 0, L))'
U_func_f_format = f'integrate(1/2*E*I*Derivative(Derivative({f},y),y)**2, (y, 0, L))'

q_list_T = q_list.copy()
q_list_T.insert(0, '0')
q_list_dot_T = q_list_dot.copy()
q_list_dot_T.insert(0, '0')

T = [[T_func_f_format, {'k1':q_list_T[0:10], 'k2':q_list_dot_T[0:10], 'k3':q_list_T[1:11], 'k4':q_list_dot_T[1:11]}]]
U = [[U_func_f_format, {'k1':q_list_T[0:10], 'k2':q_list_dot_T[0:10], 'k3':q_list_T[1:11], 'k4':q_list_dot_T[1:11]}]]


###############################################
##########   USER DEFINITION END   ############
###############################################

variable_list_str = [var_list_str, parameter_list_str]
var_raw = open('variable_list_str.pkl', 'wb')
pickle.dump(variable_list_str, var_raw)
T_raw = open('T_raw.pkl', 'wb')
pickle.dump(T, T_raw)
U_raw = open('U_raw.pkl', 'wb')
pickle.dump(U, U_raw)
IC_raw = open('IC.pkl', 'wb')
pickle.dump(IC, IC_raw)
print(T)