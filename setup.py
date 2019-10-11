from sympy import *
import pickle
from shape_gen import shape_gen

##### Put variables as a list of strings ######

var_list_str = []
parameter_list_str = ['L', 'E', 'I', 'rho', 'A']
L, E, I, rho, A = symbols('L, E, I, rho, A')

###############################################
###########     USER DEFINITION      ##########
###############################################

#######     DEFINE VARIABLE STRINGS     #######

q_list = []
q_list_dot = []
for i in range(1, 11):
    q_list.append(f'q{i}')
    q_list_dot.append(f'q{i}_dot')

var_list_str = [*q_list, *q_list_dot]

# q_list_dt = [0]
# q_list_dot_dt = [0]
# for i in range(1, 11):
#     q_list_dt.append(f'q{i}_dt')
#     q_list_dot_dt.append(f'q{i}_dot_dt')

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
T_func_f_format = f'integrate(1/2*rho*A*diff({f},t)**2, (y, 0, L))'

T = [[str(1/2*f), {k1:q_list[0:10], k2:q_list_dot[0:10], k3:q_list[1:11], k4:q_list_dot[1:11]}]]
U = [[], []]


###############################################
##########   USER DEFINITION END   ############
###############################################

print(var_list_str)
var_raw = open('var_list_str.pkl', 'wb')
pickle.dump(var_list_str, var_raw)