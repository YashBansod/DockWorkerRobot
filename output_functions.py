#!/usr/bin/env python
"""
File Description:
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division


# ****************************************        Function Declaration        **************************************** #
def text_output(params, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr):
    sim_ctrl = params['SIM_CTRL']
    if params['MODE'] == 'deterministic':
        print("\nSimulation ran %d times for %d time steps." % (sim_ctrl['N'], sim_ctrl['T_SIM_IN']))
        print("Mean service time for ships was: %2.2f minutes" % mean_s_time_arr)
        print("Mean queue wait time for ships was: %2.2f minutes" % mean_wq_time_arr)
        print("Mean queue length was: %2.2f ships" % mean_q_len_arr)
        print("Number of cargo containers transported to the city: %d containers." % num_c_arr)
        print("Number of ships serviced by the dock: %d ships." % num_s_arr)

    else:
        raise NotImplementedError


# ****************************************        Function Declaration        **************************************** #
def graph_output(params, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr):
    if params['MODE'] == 'deterministic':
        raise NotImplementedError

    else:
        raise NotImplementedError


"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""