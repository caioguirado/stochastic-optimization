from environments import Environment
from policies import Policy
from objectives import Objective


class Simulation:
    def __init__(
        self, environment: Environment, policy: Policy, objective: Objective
    ) -> None:
        pass

    def run(self, config):
        # for n_iterations
        # run full episode (environment terminal state or max T initial arg)
        # get state
        # make decision
        # update objective
        # update environment (step)
        pass
