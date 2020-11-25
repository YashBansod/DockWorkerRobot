#!/usr/bin/env python
"""
Dock Worker Robot Simulation Deterministic Test Routine.
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
import importlib.util
import argparse
import numpy as np
from tqdm import tqdm
from os.path import join
from utils import param_interpreter
from simulation_func import simulate


# ******************************************        Main Program Start      ****************************************** #
def main(args):
    """
    The main of the program.
    """
    exp_id = 'exp_0'

    param_path = join(args.dir_path, args.parameter)
    spec = importlib.util.spec_from_file_location("", param_path)
    p_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p_module)
    param_dict = param_interpreter(p_module.PARAM_DICT)
    st_params = param_dict['S_PARAMS']

    k_val_range = [('triangular', 4, 6, 7), ('triangular', 7, 9, 10), ('triangular', 10, 12, 13)]
    csp_val_range = [('triangular', 1, 3, 4), ('triangular', 3, 5, 6)]
    cpt_val_range = [('triangular', 0, 2, 3), ('triangular', 2, 4, 5)]
    cst_val_range = [('triangular', 3, 5, 6), ('triangular', 7, 9, 10)]

    num_exp = len(k_val_range) * len(csp_val_range) * len(cpt_val_range) * len(cst_val_range)

    mean_s_time_arr = np.zeros(num_exp)     # Mean service time
    mean_wq_time_arr = np.zeros(num_exp)    # Mean queue wait time
    mean_q_len_arr = np.zeros(num_exp)      # Mean queue length
    num_c_arr = np.zeros(num_exp)           # Number of cargo containers transported to city
    num_s_arr = np.zeros(num_exp)           # Number of ships processed

    np.random.seed(args.seed)

    ind = 0
    for k_val in k_val_range:
        st_params['K'] = k_val
        for csp_val in csp_val_range:
            st_params['CSP'] = csp_val
            for cpt_val in cpt_val_range:
                st_params['CPT'] = cpt_val
                for cst_val in cst_val_range:
                    st_params['CST'] = cst_val

                    _mean_s_time_arr = np.zeros(param_dict['SIM_CTRL']['N'])  # Mean service time
                    _mean_wq_time_arr = np.zeros(param_dict['SIM_CTRL']['N'])  # Mean queue wait time
                    _mean_q_len_arr = np.zeros(param_dict['SIM_CTRL']['N'])  # Mean queue length
                    _num_c_arr = np.zeros(param_dict['SIM_CTRL']['N'])  # Number of cargo containers transported to city
                    _num_s_arr = np.zeros(param_dict['SIM_CTRL']['N'])  # Number of ships processed

                    np.random.seed(args.seed)

                    for sim_num in tqdm(range(param_dict['SIM_CTRL']['N'])):
                        sim_result = simulate(param_dict)

                        _mean_s_time_arr[sim_num] = sim_result['MEAN_SERV_TIME']
                        _mean_wq_time_arr[sim_num] = sim_result['MEAN_WQ_TIME']
                        _mean_q_len_arr[sim_num] = sim_result['MEAN_Q_LEN']
                        _num_c_arr[sim_num] = sim_result['CARGO_TRANS']
                        _num_s_arr[sim_num] = sim_result['SHIPS_SERVICED']

                    mean_s_time_arr[ind] = _mean_s_time_arr.mean()
                    mean_wq_time_arr[ind] = _mean_wq_time_arr.mean()
                    mean_q_len_arr[ind] = _mean_q_len_arr.mean()
                    num_c_arr[ind] = _num_c_arr.mean()
                    num_s_arr[ind] = _num_s_arr.mean()
                    ind += 1

    if args.write:
        header = 'S_T, WQ_T, Q_L, C, S'
        output_file = np.zeros((num_exp, 5))
        output_file[:, 0] = mean_s_time_arr
        output_file[:, 1] = mean_wq_time_arr
        output_file[:, 2] = mean_q_len_arr
        output_file[:, 3] = num_c_arr
        output_file[:, 4] = num_s_arr
        # noinspection PyTypeChecker
        np.savetxt('stochastic_test_%s.txt' % exp_id, output_file, fmt='%0.2f', delimiter=', ', header=header)


# ******************************************        Main Program End        ****************************************** #
if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description='DWRS Simulator Main File.')

    argparser.add_argument('-d', '--display', action='store_true', dest='plot', help='Plot graphic results.')
    argparser.add_argument('--dir_path', default='./', type=str, help='Directory path of parameter file.')
    argparser.add_argument('-p', '--parameter', default='parameters.py', type=str, help='Name of the parameter file.')
    argparser.add_argument('-v', '--verbose', action='store_true', dest='debug', help='Print text results.')
    argparser.add_argument('-w', '--write', action='store_true', dest='write', help='Write results as pickle file.')
    argparser.add_argument('-s', '--seed', default=None, type=int, help='Set seed for repeating executions')

    sim_args = argparser.parse_args()

    print(__doc__)

    try:
        main(sim_args)
        print('\nFile executed successfully!\n')
    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""