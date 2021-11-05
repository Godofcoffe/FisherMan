class Xpaths:
    @property
    def bio(self):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/' \
               'div/div/div/div[2]/div/div/span'

    @property
    def followers(self):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/' \
               'div/div/div/div[1]/div[2]/div/div[2]/span/span'

    @property
    def friends(self):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/' \
               'div/div[1]/div/div/div/div/div/div/a[3]/div[1]'

    @property
    def picture(self):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/' \
               'div/div/div'


class Manager:
    def __init__(self):
        self.__url = 'https://www.facebook.com/'
        self.__id_url_prefix = "https://www.facebook.com/profile.php?id="
        self.__prefix_url_search = "https://www.facebook.com/search/people/?q="
        self.__fake_email = 'submarino.sub.aquatico@outlook.com'
        self.__password = 'MDBjbGVwdG9tYW5pYWNvMDA='
        self.__data = {}
        self.__affluent = {}
        self.__extras = {}

    def clean_all(self):
        """
            Clear all data.
        """
        self.__data.clear()
        self.__affluent.clear()
        self.__extras.clear()

    def clean_data(self):
        """
            Clear dict data.
        """
        self.__data.clear()

    def clean_affluent(self):
        """
            Clear affluent data.
        """
        self.__affluent.clear()

    def clean_extras(self):
        """
            Clear extras data.
        """
        self.__extras.clear()

    def set_email(self, string: str):
        """
            Defines the default email to use.

            :param string: Email.
        """
        self.__fake_email = string

    def set_pass(self, string: str):
        """
            Defines the default password to use.

            :param string: Password.
        """
        self.__password = string

    def set_data(self, dictionary: dict):
        """
            Updates the data in __date__ in its entirety.

            :param dictionary: dict to update.
        """
        self.__data = dictionary

    def set_affluent(self, dictionary: dict):
        """
            Updates the data in __affluent in its entirety.

            :param dictionary: dict to update.
        """
        self.__affluent = dictionary

    def set_extras(self, dictionary: dict):
        """
            Updates the data in __extras in its entirety.

            :param dictionary: dict to update.
        """
        self.__extras = dictionary

    def add_data(self, key, item):
        """
            Add a data in __date__ with an identifying key.

            :param key: identification key.
            :param item: data to be assigned to key.
        """
        self.__data[key] = item

    def add_affluent(self, key, item):
        """
            Add a data in __affluent with an identifying key.

            :param key: identification key.
            :param item: data to be assigned to key.
        """
        self.__affluent[key] = item

    def add_extras(self, key, item):
        """
            Add a data in __extras with an identifying key.

            :param key: identification key.
            :param item: data to be assigned to key.
        """
        self.__extras[key] = item

    def get_url(self):
        """
            Returns default class page.

            :return: default page.
        """
        return self.__url

    def get_id_prefix(self):
        """
            Returns user id link prefix.

            :return: link prefix
        """
        return self.__id_url_prefix

    def get_search_prefix(self):
        """
            Returns search prefix.

            :return: search prefix
        """
        return self.__prefix_url_search

    def get_email(self):
        """
            Returns default class email.

            :return: default email.
        """
        return self.__fake_email

    def get_pass(self):
        """
            Returns default class password.

            :return: default password.
        """
        return self.__password

    def get_data(self):
        """
            Returns all datas.

            :return: __data.
        """
        return self.__data

    def get_affluent(self):
        """
            Returns all affluents.

            :return: __affluent.
        """
        return self.__affluent

    def get_extras(self):
        """
            Returns all extras.

            :return: __extras.
        """
        return self.__extras

    def get_all_keys(self):
        """
            Return all keys from all dictionaries.

            extras, affluent, data
            To get all returns:
            datas = self.get_all_keys()

            For an individual:
            data = self.get_all_keys()[1]
        """
        return self.__extras.keys(), self.__affluent.keys(), self.__data.keys()

    def get_all_values(self):
        """
            Return all items from all dictionaries.

            extras, affluent, data
            To get all returns:
            datas = self.get_all_items()

            For an individual:
            data = self.get_all_items()[1]
        """
        return self.__extras.values(), self.__affluent.values(), self.__data.values()
