import csv
import os
import re

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

from mathematical_models.Yue2024MicroCirculation import Yue2024MicroCirculation
from utils.Configuration import Configuration
from utils.Parameters import Parameters


def find_avg_file(t_name, i_name, f_name):
    dir_name = '../data/' + t_name + '/' + i_name + '/'
    files = os.listdir(dir_name)
    for fl in files:
        if re.match(f_name, fl):
            return dir_name + fl
    return None


def calc_cir(config, c_factor, c_alpha, c_velo, c_beta):
    config.velocity = config.velocity * c_velo
    config.alpha = c_alpha * config.alpha
    config.set_parameters(p)
    paper = Yue2024MicroCirculation(p)
    cir_paper = paper.get_cir_values_interval(p.t_start, p.t_end, p.t_step)
    lists = sorted(cir_paper.items())
    theory_x, theory_y = zip(*lists)
    res_cir = [(n * c_factor) for n in theory_y]
    return res_cir


def calc_theoretic_cir(config, factor_1, factor_2, alpha_1, alpha_2, velo_1, velo_2, beta_1, beta_2):
    config_1 = config.copy_config()
    config_2 = config.copy_config()
    t_cir_1 = calc_cir(config_1, factor_1, alpha_1, velo_1, beta_1)
    t_cir_2 = calc_cir(config_2, factor_2, alpha_2, velo_2, beta_2)
    t_cir = []
    for s in range(len(t_cir_1) - 2):
        t_cir.append(t_cir_1[s] + t_cir_2[s])
    return np.array(t_cir)


def calc_mse(observed, expected):
    for i in range(len(observed)):
        if observed[i] <= 0:
            observed[i] = 0
    sub = np.subtract(expected, observed)
    squ = np.square(sub)
    mse = np.mean(squ)
    return mse


def write_results(file_name_base,
                  printed_config,
                  times,
                  data,
                  theo):
    result_file_name = file_name_base + printed_config.get_descriptor_str() + '.csv'
    with open(result_file_name, 'w') as cir_file:
        cir_writer = csv.writer(cir_file, delimiter=',')
        for i in range(len(times)):
            cir_writer.writerow([times[i]] + [data[i]] + [theo[i]])


exp_type = ['blood']
exp_injection = ['90degree']
exp_velocity = ['7,5cms']
exp_distances = ['5cm','10cm','15cm','20cm']
factor = [[1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0]]
beta = [[0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0]]
velo = [[1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0]]
alpha_mod = [[1.0,1.0,1.0,1.0], [1.0,1.0,1.0,1.0]]

num_data = len(exp_type) * len(exp_injection) * len(exp_velocity) * len(exp_distances)
i_data = 0

configs = []
timex = []
cir_data = None

for t in exp_type:
    for i in exp_injection:
        for v in exp_velocity:
            for d in exp_distances:
                file_name = '.*_' + d + '_' + v + '.*avg\.csv'
                print(file_name)
                avg_file = find_avg_file(t, i, file_name)
                x = []
                time_x = []
                cir = []
                j = 0
                if avg_file is None:
                    continue
                with open(avg_file, 'r') as csvfile:
                    plots = csv.reader(csvfile, delimiter=',')
                    first_line = True
                    for row in plots:
                        if first_line:
                            first_line = False
                            continue
                        x.append(j)
                        time_x.append(float(row[0]))
                        cir.append(float(row[1]))
                        j = j + 1
                    timex = time_x
                del x[-100:]
                del timex[-100:]
                del cir[-100:]
                configs.append(Configuration(t, i, v, d))
                if cir_data is None:
                    cir_data = np.zeros((num_data, len(timex)))
                cir_data[i_data, :] = cir
                i_data += 1
                plt.plot(timex, cir, '-', label=d)

gamma = 0
p = Parameters()
cir_theo_data = np.zeros(cir_data.shape)

for c in range(len(configs)):
    cir_measure = np.array(cir_data[c, :])
    config = configs[c]
    if config.velocity == 7.5 * (10 ** (-2)):
        base_factor = 793  # maximum frequency shift at lower speed
    else:
        base_factor = 1039  # maximum frequency shift at higher speed
    base_factor = base_factor * 0.08661 * 6
    print("base: "+str(base_factor))
    cir_theory_before = calc_theoretic_cir(config, base_factor * factor[0][c], base_factor * factor[1][c], alpha_mod[0][c], alpha_mod[1][c],
                                           velo[0][c], velo[1][c], beta[0][c], beta[1][c])
    def model(params: np.ndarray):
        global config
        global cir_measure
        factor_1 = params[0]
        factor_2 = params[1]
        print("facs: ",factor_1, factor_2)
        alpha_1 = params[2]
        alpha_2 = params[3]
        velo_1 = params[4]
        velo_2 = params[5]
        beta_1 = params[6]
        beta_2 = params[7]
        cir_theory = calc_theoretic_cir(config, factor_1, factor_2, alpha_1, alpha_2, velo_1, velo_2, beta_1, beta_2)
        return calc_mse(cir_measure, cir_theory)

    x0 = np.array([factor[0][c], factor[1][c], alpha_mod[0][c], alpha_mod[1][c],
                   velo[0][c], velo[1][c], beta[0][c], beta[1][c]])
    bnds = ((0, base_factor), (0, base_factor),  # factor to match the peak height
            (1, 1), (1, 1),  # possible modification of alpha - not used here
            (2, 157000), (0, 1),  # first peak can travel up to speed of sound, second peak can travel up to maximum speed in channel
            (0, 0), (0, 0))  # possible modification of beta - not used here
    result = optimize.minimize(fun=model, x0=x0, method='SLSQP', bounds=bnds,
                               options={'maxiter': 100000, 'disp': False})
    factor[0][c] = result.x[0] / base_factor
    factor[1][c] = result.x[1] / base_factor
    alpha_mod[0][c] = result.x[2]
    alpha_mod[1][c] = result.x[3]
    velo[0][c] = result.x[4]
    velo[1][c] = result.x[5]
    beta[0][c] = result.x[6]
    beta[1][c] = result.x[7]
    cir_theory_opt = calc_theoretic_cir(config, factor[0][c] * base_factor, factor[1][c] * base_factor, alpha_mod[0][c], alpha_mod[1][c],
                                        velo[0][c], velo[1][c], beta[0][c], beta[1][c])
    cir_theo_data[c,:] = cir_theory_opt
    plt.plot(timex, cir_theory_opt, '-', label=str(int(config.distance*100)) + 'cm fit')

    write_results('./data/_yue_', config, timex, cir_data[c,:], cir_theo_data[c,:])


print(f'exp_type = [\'{exp_type[0]}\']')
print(f'exp_injection = [\'{exp_injection[0]}\']')
print(f'exp_velocity = [\'{exp_velocity[0]}\']')
print(f'exp_distances = [\'{exp_distances[0]}\',\'{exp_distances[1]}\','
      f'\'{exp_distances[2]}\',\'{exp_distances[3]}\']')
print(f'factor = [[{factor[0][0]},{factor[0][1]},{factor[0][2]},{factor[0][3]}], '
      f'[{factor[1][0]},{factor[1][1]},{factor[1][2]},{factor[1][3]}]]')
print(f'beta = [[{beta[0][0]},{beta[0][1]},{beta[0][2]},{beta[0][3]}], '
      f'[{beta[1][0]},{beta[1][1]},{beta[1][2]},{beta[1][3]}]]')
print(f'velo = [[{velo[0][0]},{velo[0][1]},{velo[0][2]},{velo[0][3]}], '
      f'[{velo[1][0]},{velo[1][1]},{velo[1][2]},{velo[1][3]}]]')
print(f'alpha_mod = [[{alpha_mod[0][0]},{alpha_mod[0][1]},{alpha_mod[0][2]},{alpha_mod[0][3]}], '
      f'[{alpha_mod[1][0]},{alpha_mod[1][1]},{alpha_mod[1][2]},{alpha_mod[1][3]}]]')
plt.xlabel('Time')
plt.ylabel('Hz')
plt.title('CIR - ' + t + ' at ' + v + ', injection: ' + i)
plt.legend()
#plt.savefig('figures/distances_' +t+ '_'+ v + '_' + i +'.pdf')
plt.show()


