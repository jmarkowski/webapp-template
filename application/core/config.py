from os import getenv


class Config():
    def __init__(self, override_settings: dict | None = None):
        """Upon initialization, optionally load settings based on the following
        order of precedence:
        1. Environment always wins.
        2. Override settings as implemented in code.
        3. External settings as defined in the python file defined by
           SECRET_SETTINGS.
        """
        pyfile_settings_path = getattr(self, 'SECRET_SETTINGS', None)

        if pyfile_settings_path:
            self.__update_from_pyfile(pyfile_settings_path)

        if override_settings:
            self.__update_from_dict(override_settings)

        self.__update_from_env()
        self.check_config_conditions()

    @classmethod
    def check_config_conditions(cls):
        pass

    @classmethod
    def __update_from_env(cls):
        """Return a dictionary of select environment settings."""
        for k in dir(cls):
            if k.isupper():
                v = getenv(k)
                if v:
                    setattr(cls, k, v)

    @classmethod
    def __update_from_dict(cls, dct: dict):
        """Set class attributes from a given dictionary."""
        for k,v in dct.items():
            if k.isupper():
                setattr(cls, k, v)

    @classmethod
    def __update_from_pyfile(cls, pyfile_path):
        pyfile_config = dict()
        try:
            with open(pyfile_path, mode='rb') as f:
                exec(compile(f.read(), pyfile_path, 'exec'), pyfile_config)

                for k,v in pyfile_config.items():
                    if k.isupper():
                        setattr(cls, k, v)
        except FileNotFoundError as e:
            print(f'CONFIGURATION ERROR: {e}')
