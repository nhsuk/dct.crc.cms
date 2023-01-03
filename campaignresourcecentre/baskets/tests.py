from django.test import TestCase
from django.test.client import Client

from .basket import Basket
from .exceptions import ItemNotInBasketError

TEST1_ITEM_URL = "https://test.com/item1"
TEST1_IMAGE_URL = "https://test.com/assets/item1/image.png"
TEST2_ITEM_URL = "https://test.com/item2"
TEST2_IMAGE_URL = "https://test.com/assets/item2/image.png"


class TestClient(TestCase):
    def setUp(self):
        self.basket = Basket(self.client.session)

    def assert_exception(self, error, message):
        self.assertEqual(str(error.exception), message)

    def test_init_no_item_in_session(self):
        session = self.client.session
        session.save()
        basket = Basket(session)
        self.assertEqual(len(basket.contents), 0)

    def test_init_with_item_in_session(self):
        session = self.client.session
        item = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
            "quantity": 2,
        }
        session["BASKET"] = {1: item}
        session.save()
        basket = Basket(session)
        self.assertEqual(len(basket.contents), 1)

    def test_add_item(self):
        item = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item, "3")
        self.assertEqual(self.basket.get_items_count(), 1)
        self.assertEqual(self.basket.get_item_count(1), 3)
        self.basket.add_item(item, "2")
        self.assertEqual(self.basket.get_item_count(1), 2)
        self.assertEqual(self.basket.contents[1]["no_quantity"], False)
        self.assertEqual(self.basket.contents[1]["bad_quantity"], False)
        self.assertEqual(self.basket.contents[1]["quantity"], 2)
        self.basket.add_item(item, None)
        self.assertEqual(self.basket.contents[1]["no_quantity"], True)
        with self.assertRaises(KeyError):
            self.basket.contents[1]["bad_quantity"]
        with self.assertRaises(KeyError):
            self.basket.contents[1]["quantity"]
        self.basket.add_item(item, "")
        self.assertEqual(self.basket.contents[1]["no_quantity"], True)
        with self.assertRaises(KeyError):
            self.basket.contents[1]["bad_quantity"]
        with self.assertRaises(KeyError):
            self.basket.contents[1]["quantity"]
        self.basket.add_item(item, "garbage")
        self.assertEqual(self.basket.contents[1]["bad_quantity"], True)
        with self.assertRaises(KeyError):
            self.basket.contents[1]["quantity"]
        self.basket.change_item_quantity(1, None)
        self.assertEqual(self.basket.contents[1]["no_quantity"], True)
        with self.assertRaises(KeyError):
            self.basket.contents[1]["bad_quantity"]
        with self.assertRaises(KeyError):
            self.basket.contents[1]["quantity"]

    def test_change_item_quantity(self):
        item = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item, "3")
        self.basket.change_item_quantity(1, "4")
        self.assertEqual(self.basket.contents[1]["quantity"], 4)
        self.assertEqual(self.basket.contents[1]["no_quantity"], False)
        self.assertEqual(self.basket.contents[1]["bad_quantity"], False)
        self.basket.change_item_quantity(1, "6")
        self.assertEqual(self.basket.contents[1]["no_quantity"], False)
        self.assertEqual(self.basket.contents[1]["bad_quantity"], True)
        self.basket.change_item_quantity(1, "A")
        self.assertEqual(self.basket.contents[1]["no_quantity"], False)
        self.assertEqual(self.basket.contents[1]["bad_quantity"], True)
        self.basket.change_item_quantity(1, None)
        with self.assertRaises(KeyError):
            self.basket.contents[1]["bad_quantity"]
        with self.assertRaises(KeyError):
            self.basket.contents[1]["quantity"]

        with self.assertRaises(ItemNotInBasketError) as error:
            self.basket.change_item_quantity(2, 4)
        self.assert_exception(error, "Item is not added to basket!")

    def test_get_all_items(self):
        item1 = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item1, "3")
        item2 = {
            "id": 2,
            "title": "Item2",
            "item_code": "ITEM02",
            "item_url": TEST2_ITEM_URL,
            "image_url": TEST2_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item2, "2")
        self.assertEqual(len(self.basket.get_all_items()), 2)

    def test_get_items_count(self):
        item1 = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item1, "3")
        item2 = {
            "id": 2,
            "title": "Item2",
            "item_code": "ITEM02",
            "item_url": TEST2_ITEM_URL,
            "image_url": TEST2_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item2, "2")
        self.assertEqual(self.basket.get_items_count(), 2)

    def test_get_item_count(self):
        item1 = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item1, "3")
        self.assertEqual(self.basket.get_item_count(1), 3)

    def test_get_items_count_empty(self):
        item1 = {
            "id": 1,
            "title": "Item1",
            "item_code": "ITEM01",
            "item_url": TEST1_ITEM_URL,
            "image_url": TEST1_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item1, "3")
        item2 = {
            "id": 2,
            "title": "Item2",
            "item_code": "ITEM02",
            "item_url": TEST2_ITEM_URL,
            "image_url": TEST2_IMAGE_URL,
            "max_quantity": 5,
        }
        self.basket.add_item(item2, "2")
        self.basket.empty_basket()
        self.assertEqual(len(self.basket.contents), 0)
        self.assertEqual(self.basket.contents, {})
