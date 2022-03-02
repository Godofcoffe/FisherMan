class Xpaths:
    @property
    def bio(cls):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/' \
               'div/div/div/div[2]/div/div/span'

    @property
    def followers(cls):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/' \
               'div/div/div/div[1]/div[2]/div/div[2]/span/span'

    @property
    def friends(cls):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/' \
               'div/div[1]/div/div/div/div/div/div/a[3]/div[1]'

    @property
    def picture(cls):
        return '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/' \
               'div/div/div'


class Manager:
    __url_base = 'https://www.facebook.com/'
    __id_url_prefix = "https://www.facebook.com/profile.php?id="
    __prefix_url_search = "https://www.facebook.com/search/people/?q="
    __ghost_email = 'opalabrillante@gmail.com'
    __ghost_password = 'a2trMDMwMzA='
    __data = {}
    __affluent = {}
    __extras = {}

    @classmethod
    def clean_all(cls):
        """
            Clear all data.
        """
        cls.__data.clear()
        cls.__affluent.clear()
        cls.__extras.clear()

    @classmethod
    def clean_data(cls):
        """
            Clear dict data.
        """
        cls.__data.clear()

    @classmethod
    def clean_affluent(cls):
        """
            Clear affluent data.
        """
        cls.__affluent.clear()

    @classmethod
    def clean_extras(cls):
        """
            Clear extras data.
        """
        cls.__extras.clear()

    @classmethod
    def set_email(cls, string: str):
        """
            Defines the default email to use.

            :param string: Email.
        """
        cls.__ghost_email = string

    @classmethod
    def set_pass(cls, string: str):
        """
            Defines the default password to use.

            :param string: Password.
        """
        cls.__ghost_password = string

    @classmethod
    def set_data(cls, dictionary: dict):
        """
            Updates the data in __date__ in its entirety.

            :param dictionary: dict to update.
        """
        cls.__data = dictionary

    @classmethod
    def set_affluent(cls, dictionary: dict):
        """
            Updates the data in __affluent in its entirety.

            :param dictionary: dict to update.
        """
        cls.__affluent = dictionary

    @classmethod
    def set_extras(cls, dictionary: dict):
        """
            Updates the data in __extras in its entirety.

            :param dictionary: dict to update.
        """
        cls.__extras = dictionary

    @classmethod
    def add_data(cls, key, item):
        """
            Add a data in __date__ with an identifying key.

            :param key: identification key.
            :param item: data to be assigned to key.
        """
        cls.__data[key] = item

    @classmethod
    def add_affluent(cls, key, item):
        """
            Add a data in __affluent with an identifying key.

            :param key: identification key.
            :param item: data to be assigned to key.
        """
        cls.__affluent[key] = item

    @classmethod
    def add_extras(cls, key, item):
        """
            Add a data in __extras with an identifying key.

            :param key: identification key.
            :param item: data to be assigned to key.
        """
        cls.__extras[key] = item

    @classmethod
    def get_url(cls):
        """
            Returns default class page.

            :return: default page.
        """
        return cls.__url_base

    @classmethod
    def get_id_prefix(cls):
        """
            Returns user id link prefix.

            :return: link prefix
        """
        return cls.__id_url_prefix

    @classmethod
    def get_search_prefix(cls):
        """
            Returns search prefix.

            :return: search prefix
        """
        return cls.__prefix_url_search

    @classmethod
    def get_email(cls):
        """
            Returns default class email.

            :return: default email.
        """
        return cls.__ghost_email

    @classmethod
    def get_pass(cls):
        """
            Returns default class password.

            :return: default password.
        """
        return cls.__ghost_password

    @classmethod
    def get_data(cls):
        """
            Returns all datas.

            :return: __data.
        """
        return cls.__data

    @classmethod
    def get_affluent(cls):
        """
            Returns all affluents.

            :return: __affluent.
        """
        return cls.__affluent

    @classmethod
    def get_extras(cls):
        """
            Returns all extras.

            :return: __extras.
        """
        return cls.__extras

    @classmethod
    def get_all_keys(cls):
        """
            Return all keys from all dictionaries.

            extras, affluent, data
            To get all returns:
            datas = cls.get_all_keys()

            For an individual:
            data = cls.get_all_keys()[1]
        """
        return cls.__extras.keys(), cls.__affluent.keys(), cls.__data.keys()

    @classmethod
    def get_all_values(cls):
        """
            Return all items from all dictionaries.

            extras, affluent, data
            To get all returns:
            datas = cls.get_all_items()

            For an individual:
            data = cls.get_all_items()[1]
        """
        return cls.__extras.values(), cls.__affluent.values(), cls.__data.values()
