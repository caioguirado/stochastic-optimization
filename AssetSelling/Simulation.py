import yaml
from tqdm import tqdm
from argparse import ArgumentParser

from environments import Environment, AssetSellingEnvironment, AssetSellingState
from policies import Policy, SellLowPolicy
from objectives import AssetSellingObjective


class Simulation:
    def __init__(
        self,
        environment: Environment,
        policy: Policy,
        objective: AssetSellingObjective,
        config: dict = {},
    ) -> None:
        self.environment = environment
        self.policy = policy
        self.objective = objective
        self.config = config
        self.cumulative_objective = 0

    def run(self):
        # for n_iterations
        for n in range(self.config["iterations"]):
            print(f"===== iteration {n} =====")
            self.environment.reset()
            # run full episode (environment terminal state or max T initial arg)
            for t in range(self.config["time_horizon"]):
                print(f"step: {t}")
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
                self.cumulative_objective += self.objective.eval(
                    action=action, state=current_state
                )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", default=True, help="config file path")
    args = parser.parse_args()

    with open(args.file) as f:
        config = yaml.safe_load(f)

    init_state = AssetSellingState(**config["init_state"])
    environment = AssetSellingEnvironment(
        init_state=init_state, exog_params=config["exog_params"]
    )
    sell_low_policy_params = [
        p["params"] for p in config["policies"] if p["name"] == "sell_low"
    ][0]
    print(config["policies"])
    print(sell_low_policy_params)
    policy = SellLowPolicy(params=sell_low_policy_params)
    print(vars(policy))
    objective = AssetSellingObjective()
    simulation = Simulation(
        environment=environment,
        policy=policy,
        objective=objective,
        config=config["simulation"],
    )
    simulation.run()
