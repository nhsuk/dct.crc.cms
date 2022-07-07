from .exceptions import ItemNotInBasketError


class Basket:
    def __init__(self, session):
        self.session = session
        self.basket = session.get("BASKET", {})

    def _update_session_basket(self):
        self.session["BASKET"] = self.basket
        self.session.save ()

    # Basket items carry validation information in addition to the bare quantity information
    # so that templates can report the current status of the user's choices. An ad-hoc
    # implementation of what Django Forms do out-of-the-box
    # Key - no_quantity: True if no quantity provided for this item
    # Key - bad_quantity: undefined if no_quantity, otherwise True if quantity is outside range 1..maximum

    def _update_quantity(self, item, quantity):
        if quantity is None:
            item ["no_quantity"] = True
            if "bad_quantity" in item: del item ["bad_quantity"]
            if "quantity" in item: del item ["quantity"]
        else:
            item ["no_quantity"] = False
            max_quantity = item["max_quantity"]
            item ["bad_quantity"] = quantity > max_quantity
            item ["quantity"] = quantity
        return item

    def get_item(self, item_id):
        return self.basket.get (item_id)

    def add_item(self, item, quantity):
        existing_item = self.basket.get(item ["id"])
        if quantity is not None:
            total_quantity = quantity
            if existing_item:
                existing_quantity = existing_item.get ("quantity")
                total_quantity =\
                    existing_quantity + quantity if existing_quantity else None
        else:
            total_quantity = None
        item = self._update_quantity(item, total_quantity)
        self.basket[item ["id"]] = item
        self._update_session_basket()

    def remove_item(self, item_id):
        if item_id in self.basket:
            del self.basket [item_id]
            self._update_session_basket()
        else:
            raise ItemNotInBasketError ("Item is not added to basket!")

    def change_item_quantity(self, item_id, quantity):
        item = self.basket.get(item_id)
        if item:
            total_quantity = quantity
            item = self._update_quantity(item, total_quantity)
            self.basket[item.get("id")] = item
            self._update_session_basket()
        else:
            raise ItemNotInBasketError ("Item is not added to basket!")

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

    def get_title(self, item_id):
        item = self.basket.get(item_id)
        title = item["title"]
        return title
