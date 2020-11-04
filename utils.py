#!/usr/bin/env python
"""
File Description:
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
            raise NotImplementedError

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
        t_arr = np.zeros(t_sim_in, dtype=np.uint32)
        t_arr[arr_list] = 1
    else:
        raise NotImplementedError

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
        raise NotImplementedError
    else:
        raise ValueError("Invalid distribution specified.")


# ****************************************        Function Declaration        **************************************** #
def time_estimator(dist):
    """
    This function is used to get an estimate time value from a distribution.

    :param dist: An integer specifying a deterministic value or a tuple specifying a random distribution.
    :return: An estimate of time from a given distribution.
    :rtype: int
    """
    if type(dist) == int:
        return dist
    elif type(dist) == tuple:
        raise NotImplementedError
    else:
        raise ValueError("Invalid distribution specified.")


"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""