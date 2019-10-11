from sympy import *
import pickle

var_raw = open('var_list_str.pkl', 'rb')
var_list_str = pickle.load(var_raw)
print(var_list_str)

###### Generating variables of functions that are callable by its symbol ########
t = symbols('t')
var_list_func = []
for i in var_list_str:
    globals()[i] = Function(i)(t)
    var_list_func.append(globals()[i])
print(var_list_func)

###### Creating the list of symbolic representation of the symbols corresponding to their functions #######
var_list_sym = []
for i in var_list_func:
    var_list_sym.append(symbols(str(i)[0:-3]))
print(var_list_sym)

###### Creating raw derivative variables ###########
var_list_dt_raw = []
for i in var_list_func:
    var_list_dt_raw.append(diff(i, t))
var_list_dt_dt_raw = []
for i in var_list_func:
    var_list_dt_dt_raw.append(diff(diff(i, t), t))
print(var_list_dt_dt_raw)

###### Creating symbolic dt variables #######
var_list_dt = []
for i in var_list_str:
    j = i+'_dt'
    globals()[j] = symbols(j)
    var_list_dt.append(globals()[j])
var_list_dt_dt = []
for i in var_list_str:
    j = i+'_dt_dt'
    globals()[j] = symbols(j)
    var_list_dt_dt.append(globals()[j])

##### Creating maps #########
var_func_to_sym = {}
for i in range(len(var_list_func)):
    var_func_to_sym[var_list_func[i]] = var_list_sym[i]

var_list_raw_to_sym_dt = {}
for i in range(len(var_list_dt_raw)):
    var_list_raw_to_sym_dt[var_list_dt_raw[i]] = var_list_dt[i]
var_list_raw_to_sym_dt_dt = {}
for i in range(len(var_list_dt_dt_raw)):
    var_list_raw_to_sym_dt[var_list_dt_dt_raw[i]] = var_list_dt_dt[i]

print(var_func_to_sym)
print(var_list_raw_to_sym_dt)
print(var_list_raw_to_sym_dt_dt)