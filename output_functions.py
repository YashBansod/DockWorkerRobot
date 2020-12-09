#!/usr/bin/env python
"""
File Description: File defining the various outputs functions used by the simulator.
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
        ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
        ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
        ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
        ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=2)
        ax5 = plt.subplot2grid((2, 6), (1, 3), colspan=2)

        ax1.hist(mean_s_time_arr, density=False, bins=n_bins)
        _mean = mean_s_time_arr.mean()
        _std = mean_s_time_arr.std()
        ax1.axvline(_mean, color='m', linestyle="--")
        ax1.axvline(_mean + _std, color='c', linestyle="-.")
        ax1.axvline(_mean - _std, color='c', linestyle="-.")
        ax1.set(title='Mean Service Time.', xlabel='Service Time (minutes)', ylabel='Simulations')

        ax2.hist(mean_wq_time_arr, density=False, bins=n_bins)
        _mean = mean_wq_time_arr.mean()
        _std = mean_wq_time_arr.std()
        ax2.axvline(_mean, color='m', linestyle="--")
        ax2.axvline(_mean + _std, color='c', linestyle="-.")
        ax2.axvline(_mean - _std, color='c', linestyle="-.")
        ax2.set(title='Mean Queue Wait Time.', xlabel='Queue Wait Time (minutes)', ylabel='Simulations')

        ax3.hist(mean_q_len_arr, density=False, bins=n_bins)
        _mean = mean_q_len_arr.mean()
        _std = mean_q_len_arr.std()
        ax3.axvline(_mean, color='m', linestyle="--")
        ax3.axvline(_mean + _std, color='c', linestyle="-.")
        ax3.axvline(_mean - _std, color='c', linestyle="-.")
        ax3.set(title='Mean Queue Length.', xlabel='Queue Length (ships)', ylabel='Simulations')

        ax4.hist(num_c_arr, density=False, bins=n_bins)
        _mean = num_c_arr.mean()
        _std = num_c_arr.std()
        ax4.axvline(_mean, color='m', linestyle="--")
        ax4.axvline(_mean + _std, color='c', linestyle="-.")
        ax4.axvline(_mean - _std, color='c', linestyle="-.")
        ax4.set(title='Number of Containers Transported.', xlabel='Number of Containers', ylabel='Simulations')

        ax5.hist(num_s_arr, density=False, bins=n_bins)
        _mean = num_s_arr.mean()
        _std = num_s_arr.std()
        ax5.axvline(_mean, color='m', linestyle="--")
        ax5.axvline(_mean + _std, color='c', linestyle="-.")
        ax5.axvline(_mean - _std, color='c', linestyle="-.")
        ax5.set(title='Number of Ships Serviced.', xlabel='Number of Ships', ylabel='Simulations')

        plt.show()

    else:
        raise NotImplementedError


# ******************************************        Isolated Testing        ****************************************** #
if __name__ == '__main__':
    raise NotImplementedError('Isolated testing not implemented. Test it with the main simulation.')

"""
Author(s): Yash Bansod, Shivam Mishra
Repository: https://github.com/YashBansod
Organization: University of Maryland at College Park
"""