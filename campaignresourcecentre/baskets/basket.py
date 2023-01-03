from .exceptions import ItemNotInBasketError


NOT_ADDED_ERROR = "Item is not added to basket!"


class Basket:
    def __init__(self, session):
        self.session = session
        self.contents = session.get("BASKET", {})
        self._has_errors = None

    def _update_session_basket(self):
        self.session["BASKET"] = self.contents
        self.session.save()
        self._has_errors = None

    # Basket items carry validation information in addition to the bare quantity information
    # so that templates can report the current status of the user's choices. An ad-hoc
    # implementation of what Django Forms do out-of-the-box
    # Key - no_quantity: True if no quantity provided for this item
    # Key - bad_quantity: undefined if no_quantity, otherwise True if quantity is outside range 1..maximum

    def _assign_new_quantity(self, item, quantity_text):
        item["no_quantity"] = False
        previous_quantity = item.get("quantity")
        bad_quantity = not quantity_text.isdigit()
        if not bad_quantity:
            quantity = int(quantity_text)
            bad_quantity = quantity < 1
            if not bad_quantity:
                max_quantity = item["max_quantity"]
                if quantity <= max_quantity:
                    item["quantity"] = quantity
                    if previous_quantity is not None and previous_quantity != quantity:
                        item["updated"] = True
                else:
                    bad_quantity = True
        item["bad_quantity"] = bad_quantity

    def _clear_quantity(self, item):
        item["no_quantity"] = True
        if "bad_quantity" in item:
            del item["bad_quantity"]
        if "quantity" in item:
            del item["quantity"]

    def _update_quantity(self, item, quantity_text):
        if item.get("updated"):
            del item["updated"]

        if quantity_text:
            self._assign_new_quantity(item, quantity_text)
        else:
            self._clear_quantity(item)

        return item

    def get_item(self, item_id):
        return self.contents.get(item_id)

    def add_item(self, new_item, quantity_text):
        self._update_quantity(new_item, quantity_text)
        self.contents[new_item["id"]] = new_item
        self._update_session_basket()

    def remove_item(self, item_id):
        if item_id in self.contents:
            del self.contents[item_id]
            self._update_session_basket()

    def change_item_quantity(self, item_id, quantity_text):
        item = self.contents.get(item_id)
        if item:
            self._update_quantity(item, quantity_text)
            self._update_session_basket()
            return item
        else:
            raise ItemNotInBasketError(NOT_ADDED_ERROR)

    def get_all_items(self):
        return self.contents

    def get_resource_page_items(self, resource_page_id):
        return {
            id: item
            for id, item in self.contents.items()
            if item["resource_page_id"] == resource_page_id
        }

    def get_item_count(self, item_id):
        item = self.contents.get(item_id)
        if item:
            return item.get("quantity", 0)
        return 0

    def get_item_has_error(self, item_id):
        item = self.contents.get(item_id)
        if item:
            return item.get("bad_quantity") or item.get("no_quantity")

    def get_items_count(self):
        return len(self.contents)

    def empty_basket(self):
        self.contents = {}
        self._update_session_basket()

    def get_max_quantity(self, item_id):
        if item_id in self.contents:
            return self.contents[item_id]["max_quantity"]
        raise ItemNotInBasketError(NOT_ADDED_ERROR)

    def get_title(self, item_id):
        if item_id in self.contents:
            return self.contents[item_id]["title"]
        raise ItemNotInBasketError(NOT_ADDED_ERROR)

    @property
    def has_errors(self):
        if self._has_errors is None:
            error_count = sum(
                (
                    1
                    if (item[1].get("no_quantity") or item[1].get("bad_quantity"))
                    else 0
                    for item in self.contents.items()
                )
            )
            self._has_errors = error_count > 0
        return self._has_errors
