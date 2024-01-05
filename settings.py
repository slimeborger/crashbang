class Settings():

    options = {
            "lock_screen": False,
            "close_active_window": False
        }

    def __init__(self) -> None:
        ...

    @classmethod
    def set(cls , option, value):
        cls.options[option] = value
        print(f"Set {option} to {value}")

    @classmethod
    def get(cls , option):
        return(cls.options[option])
