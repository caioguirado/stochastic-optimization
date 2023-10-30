from policy import Decision, Policy


class SellLowPolicy(Policy):
    pass

    def __init__(self, params) -> None:
        super().__init__()
        self.lower_limit = params["lower_limit"]

    def eval(self, state) -> Decision:
        if state.price < self.lower_limit:
            return Decision({"sell": 1, "hold": 0})
        else:
            return Decision({"sell": 0, "hold": 1})
