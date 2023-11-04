from .policy import Decision, Policy


class SellLowPolicy(Policy):
    def __init__(self, params) -> None:
        self.lower_limit = params[0]

    def eval(self, state) -> Decision:
        if state.price < self.lower_limit:
            return Decision({"sell": 1, "hold": 0})
        else:
            return Decision({"sell": 0, "hold": 1})
