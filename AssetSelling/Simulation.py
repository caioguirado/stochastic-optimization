import yaml
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
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
        self.results = []
        self.states = []
        self.actions = []
        self.rewards = []

    def run(self):
        # for n_iterations
        for n in tqdm(range(self.config["iterations"])):
            self.environment.reset()
            self.cumulative_objective = 0

            self.states.append([])
            self.actions.append([])
            self.rewards.append([])
            # run full episode (environment terminal state or max T initial arg)
            for t in range(self.config["time_horizon"]):
                # get state
                current_state = self.environment.get_state()
                self.states[n].append(current_state)
                if current_state.is_terminal():
                    # compute statistics
                    break

                # make decision
                action = self.policy.eval(current_state).get_action()
                self.actions[n].append(action)

                # update environment (step)
                observations = self.environment.step(action)

                # update objective
                reward = self.objective.eval(action=action, state=current_state)
                self.cumulative_objective += reward
                self.rewards[n].append(reward)

            self.results.append(self.cumulative_objective)

        # save plots
        fig, axsubs = plt.subplots(1, 2, sharex=True, sharey=True)
        fig.suptitle(
            "Asset selling using policy {} with parameters {} and T {}".format(
                self.config["policy"],
                # policy_info[self.config['policy']],
                "",
                self.config["time_horizon"],
            )
        )
        i = np.arange(0, config["simulation"]["iterations"], 1)

        cum_avg_contrib = pd.Series(self.results).expanding().mean()
        axsubs[0].plot(i, cum_avg_contrib, "g")
        axsubs[0].set_title("Cumulative average contribution")

        axsubs[1].plot(i, self.results, "g")
        axsubs[1].set_title("Contribution per iteration")

        # Create a big subplot
        ax = fig.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axes
        plt.tick_params(
            labelcolor="none", top=False, bottom=False, left=False, right=False
        )

        ax.set_ylabel(
            "USD", labelpad=0
        )  # Use argument `labelpad` to move label downwards.
        ax.set_xlabel("Iterations", labelpad=10)

        # plt.show()
        plt.savefig(f"{self.config['policy']}_results_refactored.png")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", default=True, help="config file path")
    args = parser.parse_args()

    with open(args.file) as f:
        config = yaml.safe_load(f)

    init_state = AssetSellingState(**config["init_state"])
    environment = AssetSellingEnvironment(
        init_state=init_state, exog_params=config["exog_params"], seed=20180529
    )
    sell_low_policy_params = [
        p["params"] for p in config["policies"] if p["name"] == "sell_low"
    ][0]
    policy = SellLowPolicy(params=sell_low_policy_params)
    objective = AssetSellingObjective()
    simulation = Simulation(
        environment=environment,
        policy=policy,
        objective=objective,
        config=config["simulation"],
    )
    simulation.run()
