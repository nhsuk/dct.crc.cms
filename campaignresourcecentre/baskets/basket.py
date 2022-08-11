from .exceptions import MaxQuantityExceededError, ItemNotInBasketError


class Basket:
    def __init__(self, session):
        self.session = session
        self.basket = session.get("BASKET", {})

    def _update_session_basket(self):
        self.session["BASKET"] = self.basket
        self.session.save()

    def _update_quantity(self, item, quantity):
        max_quantity = item["max_quantity"]
        if quantity > max_quantity:
            raise MaxQuantityExceededError(
                "Item quantity should be less than maximum quantity!"
            )
        item["quantity"] = quantity
        return item

    def add_item(self, item, quantity):
        existing_item = self.basket.get(item.get("id"))
        total_quantity = quantity
        if existing_item:
            total_quantity = existing_item.get("quantity") + quantity
        item = self._update_quantity(item, total_quantity)
        self.basket[item.get("id")] = item
        self._update_session_basket()

    def remove_item(self, item_id):
        if item_id in self.basket:
            del self.basket[item_id]
            self._update_session_basket()

    def change_item_quantity(self, item_id, quantity):
        item = self.basket.get(item_id)
        if item:
            total_quantity = quantity
            item = self._update_quantity(item, total_quantity)
            self.basket[item.get("id")] = item
            self._update_session_basket()
        else:
            raise ItemNotInBasketError("Item is not added to basket!")

    def get_all_items(self):
        return self.basket

    def get_item_count(self, item_id):
        item = self.basket.get(item_id)
        if item:
            return item["quantity"]
        return 0

    def get_items_count(self):
        return len(self.basket)

    def empty_basket(self):
        self.basket = {}
        self._update_session_basket()

    def get_max_quantity(self, item_id):
        item = self.basket.get(item_id)
        max_quantity = item["max_quantity"]
        return max_quantity
