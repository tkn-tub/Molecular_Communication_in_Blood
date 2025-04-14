import time
import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy import optimize


def get_split_times(inj_f_name):
    times = []
    with open(inj_f_name, 'r') as f:
        injections = csv.reader(f, delimiter=',')
        for row in injections:
            s = row[0]
            t = s[20:]
            times.append(float(t))
    return times


def get_split_idx(times, time):
    for i in range(len(times)):
        t = times[i]
        if t < time:
            continue
        else:
            return i
    return -1


def write_csv_results(cir_f_name, cir_data):
    times = cir_data[0, :]
    cir = cir_data[1, :]
    with open(cir_f_name, 'w') as cir_file:
        cir_writer = csv.writer(cir_file, delimiter=',')
        for i in range(len(times)):
            cir_writer.writerow([times[i]] + [cir[i]])


def calc_lin_correction(data, size, start = 0, end = -1):
    beginning = np.mean(data[start:start+size-1])
    ending = np.mean(data[end-size:end])
    slope = (ending - beginning) / len(data[start:end])
    print(slope)
    slope_correction = []
    for i in range(len(data)):
        slope_correction.append(i * slope)
    return slope_correction

def calc_lin_func(slope, offset, times):
    lin_func = []
    for t in times:
        lin_func.append(offset + slope * t)
    return np.asarray(lin_func)


def calc_mse(observed, expected):
    sub = np.subtract(expected, observed)
    squ = np.square(sub)
    mse = np.mean(squ)
    return mse


def model(params: np.ndarray, args):
    slope = params[0]
    offset = params[1]
    data = args[0]
    times = args[1]
    lin_func = calc_lin_func(slope, offset, times)
    return calc_mse(data, lin_func)


def opt_lin_correction(data, times, slope, offset):
    x0 = np.array([slope, offset])
    args = np.array([data, times])
    bnds = ((None, None), (None, None))
    return optimize.minimize(fun=model, x0=x0, args=args, method='SLSQP', bounds=bnds,
                               options={'maxiter': 500, 'disp': False})


def proc_abs_file(file_name):
    x = []
    timex = []
    ch2_o = []
    ch2 = []
    i = 0

    with open(file_name,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        first_line = True
        for row in plots:
            if first_line:
                first_line = False
                continue
            x.append(i)
            timex.append(float(row[0]))
            ch2_o.append(float(row[1]))
            i = i + 1

    plt.plot(x[4000:5000], ch2_o[4000:5000], color='g', label="CH2")

    for i in range(len(timex)):
        ch2.append(ch2_o[i]  * -1)
    plt.plot(x[4000:5000], ch2[4000:5000], color='r', label="CH2")
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('MHz')
    plt.title('Channel 2 - Absolutwerte')
    plt.legend()
    plt.show()

    ms = [(n / 100) for n in x[1:1001]]
    blood_change = ch2[4000:5000]

    return np.array([ms, blood_change])

# process measurement data with absolute frequency shift values
# average values can then be written into output file
f_name = 'no_particles'
meas_input = '../data/blood/'+f_name+'.csv'
cir_output = '../data/blood/'+f_name+'_avg.csv'
cir = proc_abs_file(meas_input)
write_csv_results(cir_output, cir)

