from environments import Environment
from policies import Policy
from objectives import Objective


class Simulation:
    def __init__(
        self, environment: Environment, policy: Policy, objective: Objective, config
    ) -> None:
        self.environment = environment
        self.policy = policy
        self.objective = objective
        self.config = config

    def run(self):
        # for n_iterations
        for n in self.config["iterations"]:
            self.environment.reset()
            # run full episode (environment terminal state or max T initial arg)
            for t in self.config["time_horizon"]:
                # get state
                current_state = self.environment.get_state()
                if current_state.is_terminal():
                    # compute statistics
                    break

                # make decision
                action = self.policy.eval(current_state).get_action()

                # update environment (step)
                observations = self.environment.step(action)

                # update objective
                self.objective.eval(action=action, observations=observations)
