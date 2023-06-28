from enum import Enum


class ActionOrderQuantity(str, Enum):
    INCREASE = "increase"
    REDUCE = "reduce"
