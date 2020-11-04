PARAM_DICT = dict()

# Simulation Control Parameters
PARAM_DICT['SIM_CTRL'] = dict()
sim_ctrl = PARAM_DICT['SIM_CTRL']
# Number of simulation time steps (in minutes)
sim_ctrl['T_SIM_IN'] = 1440
# Number of simulations to run
sim_ctrl['N'] = 1000

# Deterministic Parameters
PARAM_DICT['D_PARAMS'] = dict()
det_params = PARAM_DICT['D_PARAMS']
# Maximum length of the queue
det_params['L'] = 20
# Number of cranes at the docking station.
det_params['C'] = 2
# Number of transportation robots at the docking station.
det_params['T'] = 4
# Number of containers each pallet on docking station can accommodate.
det_params['P'] = 15
# Mean inter-arrival time (in minutes)
det_params['A_MEAN'] = 35
# Minutes taken by the robot to transfer cargo-containers from the dock to city.
det_params['TC'] = 6

# Stochastic Parameters
PARAM_DICT['S_PARAMS'] = dict()
st_params = PARAM_DICT['S_PARAMS']
# Cargo-containers on the ship
st_params['K'] = 10
# Minutes taken to transport cargo-containers from ship to pallet.
st_params['CSP'] = 3
# Minutes taken to transport cargo-containers from pallet to transportation robot.
st_params['CPT'] = 2
# Minutes taken to transport cargo-containers from ship to transportation robot.
st_params['CST'] = 4
