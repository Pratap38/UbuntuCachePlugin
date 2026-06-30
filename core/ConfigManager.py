import json
import os


class ConfigManager:

    CONFIG_PATH = "config/config.json"

    DEFAULT_CONFIG = {

        "defaultPreset": "Safe Clean",

        "showRecommendation": True,

        "showAutoDetection": True,

        "maxThreads": 4,

        "autoClean": False

    }

    def __init__(self):

        self.config = {}

        self.load()

    def load(self):

        if not os.path.exists(

            self.CONFIG_PATH

        ):

            self.createDefault()

        with open(

            self.CONFIG_PATH,

            "r"

        ) as file:

            self.config = json.load(

                file

            )

    def createDefault(self):

        os.makedirs(

            "config",

            exist_ok=True

        )

        with open(

            self.CONFIG_PATH,

            "w"

        ) as file:

            json.dump(

                self.DEFAULT_CONFIG,

                file,

                indent=4

            )

    def get(

        self,

        key

    ):

        return self.config.get(

            key

        )

    def set(

        self,

        key,

        value

    ):

        self.config[key] = value

    def save(self):

        with open(

            self.CONFIG_PATH,

            "w"

        ) as file:

            json.dump(

                self.config,

                file,

                indent=4

            )