class BasketError(Exception):
    pass


class MaxQuantityExceededError(BasketError):
    pass


class ItemNotInBasketError(BasketError):
    pass
