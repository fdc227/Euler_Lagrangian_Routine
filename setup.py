from sympy import *
import pickle
from shape_gen import shape_gen

##### Put variables as a list of strings ######

var_list_str = []
for i in range(1, 11):
    var_list_str.append(f'q{i}')

print(var_list_str)
var_raw = open('var_list_str.pkl', 'wb')
pickle.dump(var_list_str, var_raw)


##### Express the kinetic and potential energy in terms of strings in sympy form #####
##### If expressions appear in terms of repeating patterns, write one single expression and a list of variables upon which the pattern will be applied ######

T = [[], []]
U = [[], []]

