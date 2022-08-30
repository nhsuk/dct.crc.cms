from uitestcore.page import BasePage
from uitestcore.page_element import PageElement
from selenium.webdriver.common.by import By


class CRCV3AbusePage(BasePage):

    heading_1 = PageElement(By.XPATH, "//h1")

    def all_text(self, pe):
        return "".join(self.interrogate.get_list_of_texts(pe))

    def open_page(self, url):
        self.interact.open_url(url)
        self.wait.for_page_to_load()

    def showing_400(self):
        self.wait.for_page_to_load()
        assert (
            self.interrogate.get_text(self.heading_1) == "Incorrect input"
        ), "400 page not found"
