#!/usr/bin/env python
"""
File Description:
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
import numpy as np
from tqdm import tqdm
from utils import param_interpreter, t_arr_creator
from output_functions import text_output
from parameters import PARAM_DICT
from sim_class_def import ShipQueue, Robot, Ship, Pallet, Crane, Brain


# ******************************************        Main Program Start      ****************************************** #
def main():
    """
    The main of the program.
    """
    params = param_interpreter(PARAM_DICT)
    sim_ctrl = params['SIM_CTRL']
    det_params = params['D_PARAMS']
    st_params = params['S_PARAMS']

    mean_q_len_arr = np.zeros(sim_ctrl['N'])        # Mean service time
    mean_s_time_arr = np.zeros(sim_ctrl['N'])       # Mean queue wait time
    mean_wq_time_arr = np.zeros(sim_ctrl['N'])      # Mean queue length
    num_c_arr = np.zeros(sim_ctrl['N'])             # Number of cargo containers transported to the city
    num_s_arr = np.zeros(sim_ctrl['N'])             # Number of ships processed

    for sim in tqdm(range(sim_ctrl['N'])):

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

            for crane in crane_list:
                if crane.docked_ship is None:
                    ship = ship_queue.pop_ship()
                    if ship is not None:
                        crane.docked_ship = ship.dock(t_step)
                        wq_list.append(ship.serv_start - ship.arr_time)

                if crane.working:
                    crane.continue_work()
                else:
                    work_type, work_time, to_obj = brain.decision(crane)
                    if work_type != 'None':
                        crane.initiate_work(work_type, work_time, to_obj)

                if crane.docked_ship is not None:
                    if crane.docked_ship.num_containers == 0:
                        ship = crane.docked_ship
                        crane.docked_ship = ship.undock(t_step)
                        s_list.append(ship.serv_end - ship.serv_start)

            q_arr[t_step] = len(ship_queue)

        mean_s_time_arr[sim] = np.mean(s_list)      # Mean service time
        mean_wq_time_arr[sim] = np.mean(wq_list)    # Mean queue wait time
        mean_q_len_arr[sim] = q_arr.mean()          # Mean queue length
        num_c_arr[sim] = c_var                      # Number of cargo containers transported to the city
        num_s_arr[sim] = len(s_list)                # Number of ships processed

    text_output(params, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr)


# ******************************************        Main Program End        ****************************************** #
if __name__ == '__main__':
    try:
        main()
        print('\nFile executed successfully!\n')
    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""