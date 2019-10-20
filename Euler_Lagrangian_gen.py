from sympy import *
import pickle
from multiprocessing.pool import Pool

var_raw = open('variable_list_str.pkl', 'rb')
variable_list_str = pickle.load(var_raw)
var_list_str, parameter_list_str, others = variable_list_str[0], variable_list_str[1], variable_list_str[2]

T_raw = open('T_raw.pkl', 'rb')
T_raw_list = pickle.load(T_raw)
U_raw = open('U_raw.pkl', 'rb')
U_raw_list = pickle.load(U_raw)

T_num = len(T_raw_list)
U_num = len(U_raw_list)

T_string_list = []
U_string_list = []

for n in range(T_num):
    T_str_pre = T_raw_list[n][0]
    T_replace_dict = T_raw_list[n][1]
    replacement_list = [*T_replace_dict.values()]
    # check all lists in variable_list have the same value
    l = len(replacement_list[0])
    for i in range(l):
        T_str_copy = T_str_pre
        for term in T_replace_dict:
            # print(T_replace_dict[term][i])
            T_str_replace = T_str_copy.replace(term, T_replace_dict[term][i])
            T_str_copy = T_str_replace
        T_string_list.append(T_str_copy)

for n in range(U_num):
    U_str_pre = U_raw_list[n][0]
    U_replace_dict = U_raw_list[n][1]
    replacement_list = [*U_replace_dict.values()]
    # check all lists in variable_list have the same value
    l = len(replacement_list[0])
    for i in range(l):
        U_str_copy = U_str_pre
        for term in U_replace_dict:
            U_str_replace = U_str_copy.replace(term, U_replace_dict[term][i])
            U_str_copy = U_str_replace
        U_string_list.append(U_str_copy)
print(U_string_list)

###### Generating variables of functions that are callable by its symbol ########
t = symbols('t')
var_list_func = []
for i in var_list_str:
    j = i[0:-3]
    globals()[j] = Function(j)(t)
    var_list_func.append(globals()[j])
# print(var_list_func)

###### Creating the list of symbolic representation of the symbols corresponding to their functions #######
var_list_sym = []
for i in var_list_func:
    var_list_sym.append(symbols(str(i)[0:-3]))
# print(var_list_sym)

###### Creating raw derivative variables ###########
var_list_dt_raw = []
for i in var_list_func:
    var_list_dt_raw.append(diff(i, t))
var_list_dt_dt_raw = []
for i in var_list_func:
    var_list_dt_dt_raw.append(diff(diff(i, t), t))
# print(var_list_dt_raw)

###### Creating symbolic dt variables #######
var_list_dt = []
for i in var_list_str:
    j = i[0:-3]+'_dt'
    globals()[j] = symbols(j)
    var_list_dt.append(globals()[j])
var_list_dt_dt = []
for i in var_list_str:
    j = i[0:-3]+'_dt_dt'
    globals()[j] = symbols(j)
    var_list_dt_dt.append(globals()[j])

###### Sympify parameters #######

for i in parameter_list_str:
    globals()[i] = symbols(i)

for i in others:
    globals()[i] = symbols(i)

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

replacement_map = {**var_func_to_sym, **var_list_raw_to_sym_dt, **var_list_raw_to_sym_dt_dt}

###### Sympify T and U ##########

def T_gen(i):
    T_eq_pre = sympify(T_string_list[i])
    T_eq = T_eq_pre.doit()
    print(f'T term {i+1}/{len(T_string_list)} generated')
    output = []
    for j in var_list_dt_raw:
        eq = diff(diff(T_eq, j), t)
        output.append(eq.xreplace(replacement_map))
    return output

def U_gen(i):
    U_eq_pre = sympify(U_string_list[i])
    U_eq_un = U_eq_pre.doit()
    U_eq = U_eq_un.xreplace(replacement_map)
    print(f'U_term {i+1}/{len(U_string_list)} generated')
    output = []
    for j in var_list_sym:
        eq = diff(U_eq, j)
        output.append(eq)
    return output

p = Pool(len(T_string_list))
T_r = [r for r in range(len(T_string_list))]
U_r = [r for r in range(len(U_string_list))]
T_list = p.map(T_gen, T_r)
U_list = p.map(U_gen, U_r)
print(U_list)

T_final = []
for j in range(len(T_list[0])):
    local_sum_list = []
    for i in range(len(T_list)):
        local_sum_list.append(T_list[i][j])
    local_sum = sum(local_sum_list)
    T_final.append(local_sum)

U_final = []
for j in range(len(U_list[0])):
    local_sum_list = []
    for i in range(len(U_list)):
        local_sum_list.append(U_list[i][j])
    local_sum = sum(local_sum_list)
    U_final.append(local_sum)

T_raw = open('T_final.pkl', 'wb')
pickle.dump(T_final, T_raw)
U_raw = open('U_final.pkl', 'wb')
pickle.dump(U_final, U_raw)






