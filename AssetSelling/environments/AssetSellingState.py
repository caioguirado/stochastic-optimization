from .Environment import State


class AssetSellingState(State):
    def __init__(self, price: int, resource: int, bias: str, *args) -> None:
        self.price = price
        self.resource = resource
        self.bias = bias

    def is_terminal(self) -> bool:
        return self.resource == 0
