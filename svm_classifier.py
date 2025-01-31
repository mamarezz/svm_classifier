import numpy as np
import pandas as pd
from scipy.optimize import minimize


def map_values(column, mapping):
    return column.map(mapping)

def apply_mapping(value, mapping):
    return mapping.get(value, value)


file_path = r"/content/Breast_Cancer_dataset_2.txt"
data = pd.read_csv(file_path, header=None)


age_mapping = {"'10-19'": 0, "'20-29'": 1, "'30-39'": 2, "'40-49'": 3, "'50-59'": 4,
               "'60-69'": 5, "'70-79'": 6, "'80-89'": 7, "'90-99'": 8}
menopause_mapping = {"'lt40'": 0, "'ge40'": 1, "'premeno'": 2}
tumor_size_mapping = dict(zip([f"'{i}-{i+4}'" for i in range(0, 55, 5)], range(12)))
inv_nodes_mapping = dict(zip([f"'{i}-{i+2}'" for i in range(0, 40, 3)], range(14)))
node_caps_mapping = {"'yes'": 0, "'no'": 1}
deg_malig_mapping = {"'1'": 0, "'2'": 1, "'3'": 2}
breast_mapping = {"'left'": 0, "'right'": 1}
breast_quad_mapping = {"'left_up'": 0, "'left_low'": 1, "'right_up'": 2, "'right_low'": 3, "'central'": 4}
class_mapping = {"'no-recurrence-events'": -1, "'recurrence-events'": 1}
irradiat_mapping = {"'yes'": 0, "'no'": 1}



data[0] = map_values(data[0], age_mapping)
data[1] = map_values(data[1], menopause_mapping)
data[2] = map_values(data[2], tumor_size_mapping)
data[3] = map_values(data[3], inv_nodes_mapping)
data[4] = map_values(data[4], node_caps_mapping)
data[5] = map_values(data[5], deg_malig_mapping)
data[6] = map_values(data[6], breast_mapping)
data[7] = map_values(data[7], breast_quad_mapping)
data[8] = data[8].apply(lambda x: apply_mapping(x, irradiat_mapping))
data[9] = data[9].map(class_mapping)

data_features_2  = data.iloc[:, :-1].values
real_y = data.iloc[:, -1].values


print(data.head())


import numpy as np
from scipy.optimize import minimize
import re

def dual(u,points,y):

    summ=0
    u_total = 0
    for k in range(len(points)):
         u_total +=u[k]
    for i in range(len(points)):
        for j in range(len(points)):
            summ+=y[i]*y[j]*u[i]*u[j]*np.dot(points[i],points[j].T)

    return -(u_total-0.5*(summ))


def constraint(u,points,y):

    summ=0
    for i in range(len(points)):
        summ+=u[i]*y[i]
    return summ

def optimize(data, y):
    eq_cons = {'type': 'eq', 'fun': lambda x: constraint(x, data, y)}
    svm_lamda = lambda x: dual(x, data, y)
    x0 = [1] * len(data)

    opt = minimize(svm_lamda, x0, bounds=[(0, 5000) for _ in range(len(data))], constraints=eq_cons)
    u = opt.x

    w = np.zeros((data[0].shape[1], 1))
    for i in range(len(data)):
        w += u[i] * y[i] * data[i].T

    selected_u_no = next(i for i, ui in enumerate(u) if ui > 0)
    b = y[selected_u_no] - np.dot(data[selected_u_no], w)
    b = b[0][0]

    def svm_func(x):
        return 1 if ((np.dot(x, w) + b) > 0) else -1

    return w, b, svm_func


def line(w,b):
    # result = re.sub(r'\[|\]', '', expression)
    print(re.sub(r'\[|\]','',f"{w[0]}x + {w[1]}y + {b+1}"))
    print(re.sub(r'\[|\]','',f"{w[0]}x + {w[1]}y + {b}"))
    print(re.sub(r'\[|\]','',f"{w[0]}x + {w[1]}y + {b-1}"))



def test(data, svm,y) :
    right = 0
    for i in range(len(data)):
        if y[i] == svm(data[i][0]):
            right += 1
    return right / len(data)*100




data = [0 for i in range(len(data_features_2))]
for i in range(len(data)):
    data[i]=np.array([data_features_2[i]])


indices = [111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121,
           250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267]
select_data = [data[i] for i in indices]
y = [real_y[i] for i in indices]


data_test = [0 for i in range(50)]
y_test = []
for i in range(50):
    data_test[i]=np.array([data_features_2[i]])
    y_test.append(real_y[i])

w, b, svm = optimize(select_data, y_test)
line(w, b)


print(test(select_data, svm_func, y))