#!/usr/bin/env python
"""
File Description: File defining various utility functions used in the simulation.
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
import numpy as np


# ****************************************        Function Declaration        **************************************** #
def param_interpreter(params):
    """
    This function is used to interpret the parameter dictionary.

    :param dict params: A dictionary containing parameters.
    :return: The modified parameter dictionary.
    """
    st_params = params['S_PARAMS']

    det_cond = type(st_params['K']) == int and type(st_params['CSP']) == int and \
        type(st_params['CPT']) == int and type(st_params['CST']) == int

    if 'MODE' in params.keys():
        if params['MODE'] == 'deterministic' and not det_cond:
            if type(st_params['K']) != int:
                raise NotImplementedError
            elif type(st_params['CSP']) != int:
                raise NotImplementedError
            elif type(st_params['CPT']) != int:
                raise NotImplementedError
            elif type(st_params['CST']) != int:
                raise NotImplementedError

        elif params['MODE'] == 'stochastic' and det_cond:
            raise ValueError("Invalid distributions defined for stochastic parameters in stochastic mode.")

    else:
        if det_cond:
            params['MODE'] = 'deterministic'
        else:
            params['MODE'] = 'stochastic'

    return params


# ****************************************        Function Declaration        **************************************** #
def t_arr_creator(params):
    """
    This function is used to create the t_arr array. The t_arr tells if a ship arrival happens at given time step.

    :param dict params: A dictionary containing parameters.
    :return: A 1-D numpy array denoting t_arr.
    """
    if params['MODE'] == 'deterministic':
        a_mean = params['D_PARAMS']['A_MEAN']
        t_sim_in = params['SIM_CTRL']['T_SIM_IN']
        arr_list = np.arange(start=a_mean, stop=t_sim_in, step=a_mean)
    elif params['MODE'] == 'stochastic':
        a_mean = params['D_PARAMS']['A_MEAN']
        t_sim_in = params['SIM_CTRL']['T_SIM_IN']
        arr_list = random_generator(('exponential', a_mean), sz=t_sim_in)
        arr_list = np.cumsum(arr_list)
        assert arr_list[-1] >= t_sim_in
        arr_list = arr_list[arr_list < t_sim_in]
    else:
        raise NotImplementedError

    t_arr = np.zeros(t_sim_in, dtype=np.uint32)
    t_arr[arr_list] = 1

    return t_arr


# ****************************************        Function Declaration        **************************************** #
def dist_interpreter(dist):
    """
    This function is used to sample a value from a distribution.

    :param dist: An integer specifying a deterministic value or a tuple specifying a random distribution.
    :return: A sample from the distribution.
    :rtype: int
    """
    if type(dist) == int:
        return dist
    elif type(dist) == tuple:
        return random_generator(dist)[0]
    else:
        raise ValueError("Invalid distribution specified.")


# ****************************************        Function Declaration        **************************************** #
def random_generator(dist, sz=1):
    """
    This function is used to sample a value from a random distribution.

    :param dist: A tuple specifying a random distribution.
    :param sz: An integer specifying the number of values to generate
    :return: A sample from the distribution.
    :rtype: ndarray
    """
    dist_type = dist[0].lower()
    dist_args = dist[1:]

    if dist_type == 'uniform':
        val = np.ceil(np.random.uniform(*dist_args, size=sz)).astype(np.int)
    elif dist_type == 'triangular':
        val = np.ceil(np.random.triangular(*dist_args, size=sz)).astype(np.int)
    elif dist_type == 'exponential':
        val = np.ceil(np.random.exponential(*dist_args, size=sz)).astype(np.int)
    elif dist_type == 'normal':
        val = np.ceil(np.random.normal(*dist_args, size=sz)).astype(np.int)
    else:
        raise NotImplementedError("Procedure to handle the given distribution is not implemented.")
    return val


# ****************************************        Function Declaration        **************************************** #
def time_estimator(dist):
    """
    This function is used to get an estimate time value from a distribution.

    :param dist: An integer specifying a deterministic value or a tuple specifying a random distribution.
    :return: An estimate of time from a given distribution.
    :rtype: int
    """
    if type(dist) == int:
        val = dist
    elif type(dist) == tuple:
        dist_type = dist[0].lower()
        dist_args = dist[1:]
        # 90th percentile / 0.9 quantile
        if dist_type == 'uniform':
            val = dist_args[0] + 0.9 * (dist_args[1] - dist_args[0])
        elif dist_type == 'triangular':
            val = dist_args[2] - np.sqrt((dist_args[2] - dist_args[0]) * (dist_args[2] - dist_args[1]) * 0.1)
        elif dist_type == 'exponential':
            val = -np.log(0.1) * dist_args[0]
        elif dist_type == 'normal':
            # TODO: Implement the Quantile function for Normal distribution
            val = dist_args[1] + 1.282 * dist_args[1]
        else:
            raise NotImplementedError("Procedure to handle the given distribution is not implemented.")
    else:
        raise ValueError("Invalid distribution specified.")
    return val


# ******************************************        Isolated Testing        ****************************************** #
if __name__ == '__main__':
    raise NotImplementedError('Isolated testing not implemented. Test it with the simulation function.')

"""
Author(s): Yash Bansod, Shivam Mishra
Repository: https://github.com/YashBansod
Organization: University of Maryland at College Park
"""