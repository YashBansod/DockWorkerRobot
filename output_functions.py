#!/usr/bin/env python
"""
File Description:
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
from matplotlib import pyplot as plt


# ****************************************        Function Declaration        **************************************** #
def text_output(params, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr):
    sim_ctrl = params['SIM_CTRL']
    if params['MODE'] == 'deterministic':
        print("\nSimulation ran %d times for %d time steps." % (sim_ctrl['N'], sim_ctrl['T_SIM_IN']))
        print("Mean service time for ships was: %2.2f minutes" % mean_s_time_arr.mean())
        print("Mean queue wait time for ships was: %2.2f minutes" % mean_wq_time_arr.mean())
        print("Mean queue length was: %2.2f ships" % mean_q_len_arr.mean())
        print("Number of cargo containers transported to the city: %d containers." % num_c_arr.mean())
        print("Number of ships serviced by the dock: %d ships." % num_s_arr.mean())

    elif params['MODE'] == 'stochastic':
        print("\nSimulation ran %d times for %d time steps." % (sim_ctrl['N'], sim_ctrl['T_SIM_IN']))
        print("\nMean service time for ships was: %2.2f minutes" % mean_s_time_arr.mean())
        print("Standard deviation of service time for ships was: %2.2f minutes" % mean_s_time_arr.std())

        print("\nMean queue wait time for ships was: %2.2f minutes" % mean_wq_time_arr.mean())
        print("Standard deviation of queue wait time for ships was: %2.2f minutes" % mean_wq_time_arr.std())

        print("\nMean queue length was: %2.2f ships" % mean_q_len_arr.mean())
        print("Standard deviation of queue length was: %2.2f ships" % mean_q_len_arr.std())

        print("\nNumber of cargo containers transported to the city: %2.2f containers." % num_c_arr.mean())
        print("Standard deviation of number of cargo containers transported: %2.2f containers" % num_c_arr.std())

        print("\nNumber of ships serviced by the dock: %2.2f ships." % num_s_arr.mean())
        print("Standard deviation of number of ships serviced by the dock: %2.2f ships" % num_s_arr.std())

    else:
        raise NotImplementedError


# ****************************************        Function Declaration        **************************************** #
def graph_output(params, mean_s_time_arr, mean_wq_time_arr, mean_q_len_arr, num_c_arr, num_s_arr):
    sim_ctrl = params['SIM_CTRL']
    if params['MODE'] == 'deterministic':
        raise NotImplementedError
    elif params['MODE'] == 'stochastic':
        n_bins = 21
        fig, axs = plt.subplots(3, 2, tight_layout=True)
        axs[0, 0].hist(mean_s_time_arr, density=False, bins=n_bins)
        axs[0, 1].hist(mean_wq_time_arr, density=False, bins=n_bins)
        axs[1, 0].hist(mean_q_len_arr, density=False, bins=n_bins)
        axs[1, 1].hist(num_c_arr, density=False, bins=n_bins)
        axs[2, 0].hist(num_s_arr, density=False, bins=n_bins)
        # axs[0, 0].title('Histogram of Sevice Time')
        # axs[0, 0].ylabel('Probability')
        # axs[0, 0].xlabel('Service time')
        plt.show()

    else:
        raise NotImplementedError


"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""