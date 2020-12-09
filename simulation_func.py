#!/usr/bin/env python
"""
File Description: File defining the simulation function used for DWRS. This function is run N number of times in the
    main_simulation.
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
import numpy as np
from tqdm import tqdm
from utils import param_interpreter, t_arr_creator
from output_functions import text_output
from parameters import PARAM_DICT
from sim_class_def import ShipQueue, Robot, Ship, Pallet, Crane, Brain


# ****************************************        Function Declaration        **************************************** #
def simulate(params):
    """
    Function that implements the simulation
    """
    sim_ctrl = params['SIM_CTRL']
    det_params = params['D_PARAMS']
    st_params = params['S_PARAMS']

    t_arr = t_arr_creator(params)
    q_arr = np.zeros(sim_ctrl['T_SIM_IN'], dtype=np.uint32)
    wq_list, s_list = [], []
    c_var = 0

    ship_queue = ShipQueue(max_length=det_params['L'])
    crane_list = [Crane(pallet=Pallet(capacity=det_params['P'])) for _ in range(det_params['C'])]
    robot_list = [Robot(work_time=det_params['TC']) for _ in range(det_params['T'])]

    brain = Brain(params, robot_list)

    for t_step in range(sim_ctrl['T_SIM_IN']):
        if t_arr[t_step]:
            ship_queue.add_ship(Ship(arrival_time=t_step, num_containers=st_params['K']))

        for robot in robot_list:
            if robot.working:
                c_var += robot.continue_work()

        crane_list.sort()
        for crane in crane_list:
            if crane.docked_ship is None:
                ship = ship_queue.pop_ship()
                if ship is not None:
                    crane.docked_ship = ship.dock(t_step)
                    wq_list.append(ship.serv_start - ship.arr_time)
            else:
                if crane.docked_ship.num_containers == 0:
                    ship = crane.docked_ship
                    crane.docked_ship = ship.undock(t_step)
                    s_list.append(ship.serv_end - ship.serv_start)

            if crane.working:
                crane.continue_work()
            else:
                work_type, work_time, to_obj = brain.decision(crane)
                if work_type != 'None':
                    crane.initiate_work(work_type, work_time, to_obj)
                    crane.continue_work()

        q_arr[t_step] = len(ship_queue)

    result = dict()
    result['MEAN_SERV_TIME'] = np.mean(s_list)      # Mean service time
    result['MEAN_WQ_TIME'] = np.mean(wq_list)       # Mean queue wait time
    result['MEAN_Q_LEN'] = q_arr.mean()             # Mean queue length
    result['CARGO_TRANS'] = c_var                   # Number of cargo containers transported to city
    result['SHIPS_SERVICED'] = len(s_list)          # Number of ships processed
    return result


# ******************************************    Test run definition     ********************************************** #
if __name__ == '__main__':
    try:
        param_dict = param_interpreter(PARAM_DICT)
        mean_s_time_arr = np.zeros(param_dict['SIM_CTRL']['N'])     # Mean service time
        mean_wq_time_arr = np.zeros(param_dict['SIM_CTRL']['N'])    # Mean queue wait time
        mean_q_len_arr = np.zeros(param_dict['SIM_CTRL']['N'])      # Mean queue length
        num_c_arr = np.zeros(param_dict['SIM_CTRL']['N'])           # Number of cargo containers transported to city
        num_s_arr = np.zeros(param_dict['SIM_CTRL']['N'])           # Number of ships processed

        for sim_num in tqdm(range(param_dict['SIM_CTRL']['N'])):

            sim_result = simulate(param_dict)

            mean_s_time_arr[sim_num] = sim_result['MEAN_SERV_TIME']
            mean_wq_time_arr[sim_num] = sim_result['MEAN_WQ_TIME']
            mean_q_len_arr[sim_num] = sim_result['MEAN_Q_LEN']
            num_c_arr[sim_num] = sim_result['CARGO_TRANS']
            num_s_arr[sim_num] = sim_result['SHIPS_SERVICED']

        text_output(param_dict, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr)

        print('\nFile executed successfully!\n')
        # input("Press any key to exit.")
    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author(s): Yash Bansod, Shivam Mishra
Repository: https://github.com/YashBansod
Organization: University of Maryland at College Park
"""