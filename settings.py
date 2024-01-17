class Settings():
    """Getter/Setter Class that stores all settings used by Crashbang:"""

    options = {
            "lock_screen": False,
            "close_active_window": False
        }
    
    def __init__(self) -> None:
        ...

    @classmethod
    def set(cls , option, value):
        """
        Set an **option** (if exists) to a **value**
        
        :param option: Config options from a dict
        :type option: str
        :param value: Mostly bool, sometimes int
        :type value: bool or int
        """

        cls.options[option] = value

    @classmethod
    def get(cls , option):
        """
        Return the **value** associated with the key **option**

        :param option: An existing option from a dict
        :type option: str
        :return: value
        :rtype: bool or int
        """
        return(cls.options[option])
    
obj = Settings()

