from sympy import *
import pickle

##### Put variables as a list of strings ######

var_list_str = []
for i in range(1, 11):
    var_list_str.append(f'q{i}')

print(var_list_str)
var_raw = open('var_list_str.pkl', 'wb')
pickle.dump(var_list_str, var_raw)


##### Express the kinetic and potential energy in terms of strings in sympy form #####

T = ''
U = ''

