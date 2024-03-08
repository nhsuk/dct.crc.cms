class UsersPaginationWrapper:
    """
    Wrapper class to provide compatability with pagination_nav.html template
    This template expects the following attributes to exist:
    number - current page number,
    paginator - this should provide a sub-attrbute of num_pages
    has_previous, previous_page_number, has_next, next_page_number
    """

    def __init__(self, users, num_pages, page_number):
        self.users = users
        self.num_pages = num_pages
        self.page_number = page_number

    def number(self):
        return self.page_number

    def paginator(self):
        return {"num_pages": self.num_pages}

    def has_previous(self):
        if self.page_number > 1:
            return True
        else:
            return False

    def previous_page_number(self):
        if self.page_number > 1:
            return self.page_number - 1
        else:
            return 1

    def has_next(self):
        if self.page_number < self.num_pages:
            return True
        else:
            return False

    def next_page_number(self):
        if self.page_number < self.num_pages:
            return self.page_number + 1
        else:
            return self.num_pages

    def __getitem__(self, key):
        return self.users[key]

    def __len__(self):
        return len(self.users)
