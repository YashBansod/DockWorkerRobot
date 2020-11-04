#!/usr/bin/env python
"""
File Description:
"""

# ******************************************    Libraries to be imported    ****************************************** #
from __future__ import print_function, division
from collections import deque
from utils import dist_interpreter, time_estimator


# ******************************************    Class Declaration Start     ****************************************** #
class ShipQueue(object):
    """
    ShipQueue Class
    """

    def __init__(self, max_length):
        """
        Constructor of ShipQueue Class.

        :param int max_length: Maximum possible length of the ship queue.
        """
        self.max_len = max_length
        self.num_balk = 0
        self._queue = deque()

    # ******************************        Class Method Declaration        ****************************************** #
    def __len__(self):
        return len(self._queue)

    # ******************************        Class Method Declaration        ****************************************** #
    def add_ship(self, ship_obj):
        """
        Add a ship to the queue.

        :param Ship ship_obj: An object of type Ship.
        """
        # Ship balks if the queue is full.
        if len(self._queue) >= self.max_len:
            self.num_balk += 1
        else:
            self._queue.append(ship_obj)

    # ******************************        Class Method Declaration        ****************************************** #
    def pop_ship(self):
        if len(self._queue) > 0:
            return self._queue.popleft()
        else:
            return None

# ******************************************    Class Declaration End       ****************************************** #


# ******************************************    Class Declaration Start     ****************************************** #
class Robot(object):
    """
    Robot Class
    """

    def __init__(self, work_time):
        """
        Constructor of Robot Class.

        :param int work_time: Total time required to complete a work.
        """
        self.working = False
        self.locked = False
        self.work_time = work_time
        self._rem_time = 0

    # ******************************        Class Method Declaration        ****************************************** #
    def initiate_work(self):
        """
        Initiate work routine for Robot.
        """
        self.working = True
        self.locked = False
        self._rem_time = self.work_time

    # ******************************        Class Method Declaration        ****************************************** #
    def continue_work(self):
        """
        Continue work routine for Robot.

        :return: True if work was completed else False
        """
        self._rem_time -= 1

        if self._rem_time == 0:
            self.working = False
            return True
        return False

    # ******************************        Class Method Declaration        ****************************************** #
    def connect(self):
        """
        Routine to connect a Robot.
        Robot should be connected to a Crane when initiating a CST or CPT work.
        """
        self.locked = True
        return self

    # ******************************        Class Method Declaration        ****************************************** #
    def get_remaining_time(self):
        return self._rem_time

# ******************************************    Class Declaration End       ****************************************** #


# ******************************************    Class Declaration Start     ****************************************** #
class Ship(object):
    """
    Ship Class
    """

    def __init__(self, arrival_time, num_containers):
        """
        Constructor of Ship Class.

        :param int arrival_time: Time step at which ship arrives.
        :param int or tuple num_containers: Total number of cargo-containers on the ship.
        """
        self.arr_time = arrival_time
        self.num_containers = dist_interpreter(num_containers)
        self.serv_start = -1
        self.serv_end = -1

    # ******************************        Class Method Declaration        ****************************************** #
    def dock(self, curr_time):
        """
        Routine to dock a Ship.
        Ship should be docked to a Crane when initiating a CST or CSP work.

        :param int curr_time: Current time step.
        """
        self.serv_start = curr_time
        return self

    # ******************************        Class Method Declaration        ****************************************** #
    def undock(self, curr_time):
        """
        Routine to undock a Ship.
        Ship should be undocked when it is empty.

        :param int curr_time: Current time step.
        """
        self.serv_end = curr_time
        return None

# ******************************************    Class Declaration End       ****************************************** #


# ******************************************    Class Declaration Start     ****************************************** #
class Pallet(object):
    """
    Pallet Class
    """

    def __init__(self, capacity):
        """
        Constructor of Pallet Class.

        :param int capacity: Total pallet capacity.
        """
        self.capacity = capacity
        self.num_containers = 0

# ******************************************    Class Declaration End       ****************************************** #


# ******************************************    Class Declaration Start     ****************************************** #
class Crane(object):
    """
    Crane Class
    """

    def __init__(self, pallet):
        """
        Constructor of Crane Class.

        :param Pallet pallet: A pallet connected to this crane. Crane will work on this pallet.
        """
        self.working = False
        self.work_type = 'None'
        self.work_time = -1
        self._rem_time = -1
        self.pallet = pallet
        self.docked_ship = None
        self.from_obj = None
        self.to_obj = None

    # ******************************        Class Method Declaration        ****************************************** #
    def initiate_work(self, work_type, work_time, to_obj):
        """
        Initiate work routine for Crane.

        :param str work_type: One of {"CSP", "CPT", "CST"} specifying the type of work done by the crane.
        :param int work_time: Denotes the service time associated with the work.
        :param Pallet or Robot to_obj: Points to an object where the crane will unload a cargo container.
        """
        self.working = True
        self.work_type = work_type
        self.work_time = work_time
        self._rem_time = work_time

        if work_type == 'CSP':
            assert to_obj is self.pallet
            self.from_obj = self.docked_ship
            self.to_obj = to_obj

        elif work_type == 'CPT':
            assert type(to_obj) == Robot
            self.from_obj = self.pallet
            self.to_obj = to_obj.connect()

        else:
            assert type(to_obj) == Robot
            self.from_obj = self.docked_ship
            self.to_obj = to_obj.connect()

        assert self.from_obj.num_containers > 0
        self.from_obj.num_containers -= 1

    # ******************************        Class Method Declaration        ****************************************** #
    def continue_work(self):
        """
        Continue work routine for Crane.

        :return: True if work was completed else False
        """
        self._rem_time -= 1

        if self._rem_time == 0:
            if self.work_type == "CSP":
                assert self.to_obj.num_containers < self.to_obj.capacity
                self.to_obj.num_containers += 1

            else:                           # This also implies that to_obj is a Robot
                assert self.to_obj.locked

                # If the to_obj is locked but hasn't completed its previous task yet, then wait for it.
                if self.to_obj.working:
                    self._rem_time += 1
                    return False

                # Robot can initiate its task if it is loaded.
                self.to_obj.initiate_work()

            self.working = False
            self.work_type = 'None'
            self.work_time = -1
            self.from_obj = None
            self.to_obj = None
            return True
        return False

# ******************************************    Class Declaration End       ****************************************** #


# ******************************************    Class Declaration Start     ****************************************** #
class Brain(object):
    """
    Brain Class
    """

    def __init__(self, params, robot_list):
        """
        Constructor of Brain Class.

        :param dict params: A dictionary containing parameters.
        :param list[Robot] robot_list: The list of robots at the docking station.
        """
        self.params = params
        self.robot_list = robot_list

    # ******************************        Class Method Declaration        ****************************************** #
    def decision(self, crane):
        """
        The decision function. This function is used to decide the task that a given crane should do.
        :param Crane crane: The crane for which a work decision should to be taken.
        :return: A tuple specifying (work_type, work_time, to_obj)
        """
        # If a ship is docked to the crane
        if crane.docked_ship is not None:
            # Search for an available robot to transfer the container to.
            cst_time = dist_interpreter(self.params['S_PARAMS']['CST'])
            for robot in self.robot_list:
                if not robot.locked:
                    if not robot.working:
                        return 'CST', cst_time, robot
                    elif robot.get_remaining_time() <= time_estimator(self.params['S_PARAMS']['CST']):
                        return 'CST', cst_time, robot

            # Else, search for an available pallet to transfer the container to.
            csp_time = dist_interpreter(self.params['S_PARAMS']['CSP'])
            if crane.pallet.num_containers < crane.pallet.capacity:
                return 'CSP', csp_time, crane.pallet

        # If no ship is docked to the crane and the pallet is not empty
        elif crane.pallet.num_containers > 0:
            # Search for an available robot to transfer the container to.
            cpt_time = dist_interpreter(self.params['S_PARAMS']['CPT'])
            for robot in self.robot_list:
                if not robot.locked:
                    if not robot.working:
                        return 'CPT', cpt_time, robot
                    elif robot.get_remaining_time() <= time_estimator(self.params['S_PARAMS']['CST']):
                        return 'CPT', cpt_time, robot
        return 'None', -1, None

# ******************************************    Class Declaration End       ****************************************** #


"""
Author(s): <First> <Last>
Repository: https://github.com/
Organization: University of Maryland at College Park
"""