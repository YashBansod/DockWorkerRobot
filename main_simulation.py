#!/usr/bin/env python
"""
Dock Worker Robot Simulation.
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
import importlib.util
import argparse
import numpy as np
from tqdm import tqdm
from os.path import join
from utils import param_interpreter
from output_functions import text_output, graph_output
from simulation_func import simulate


# ******************************************        Main Program Start      ****************************************** #
def main(args):
    """
    The main of the program.
    """
    param_path = join(args.dir_path, args.parameter)
    spec = importlib.util.spec_from_file_location("", param_path)
    p_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p_module)
    param_dict = param_interpreter(p_module.PARAM_DICT)

    mean_s_time_arr = np.zeros(param_dict['SIM_CTRL']['N'])     # Mean service time
    mean_wq_time_arr = np.zeros(param_dict['SIM_CTRL']['N'])    # Mean queue wait time
    mean_q_len_arr = np.zeros(param_dict['SIM_CTRL']['N'])      # Mean queue length
    num_c_arr = np.zeros(param_dict['SIM_CTRL']['N'])           # Number of cargo containers transported to city
    num_s_arr = np.zeros(param_dict['SIM_CTRL']['N'])           # Number of ships processed

    np.random.seed(args.seed)

    for sim_num in tqdm(range(param_dict['SIM_CTRL']['N'])):
        sim_result = simulate(param_dict)

        mean_s_time_arr[sim_num] = sim_result['MEAN_SERV_TIME']
        mean_wq_time_arr[sim_num] = sim_result['MEAN_WQ_TIME']
        mean_q_len_arr[sim_num] = sim_result['MEAN_Q_LEN']
        num_c_arr[sim_num] = sim_result['CARGO_TRANS']
        num_s_arr[sim_num] = sim_result['SHIPS_SERVICED']

    if args.debug:
        text_output(param_dict, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr)

    if args.plot:
        graph_output(param_dict, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr)


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
        # input("Press any key to exit.")
    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""