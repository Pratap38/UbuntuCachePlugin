

import json
from pathlib import Path


class GuardianConfig:

    DEFAULT_CONFIG = {

        "enabled": True,

        "warningThreshold": 80,

        "criticalThreshold": 90,

        "emergencyThreshold": 97,

        "monitorInterval": 2,

        "autoPause": True,

        "autoResume": True,

        "desktopNotifications": True,

        "logEvents": True,

        "whitelist": [

            "systemd",

            "gnome-shell",

            "Xorg",

            "pipewire",

            "dbus-daemon",

            "NetworkManager",

            "RAM Guardian"

        ]

    }

    def __init__(self):

        self.configPath = (

            Path(__file__).parent

            / "config"

            / "guardian_config.json"

        )

        self.config = {}

        self.load()

    # -----------------------------------------------------

    def load(self):
        """
        Load configuration from JSON.
        """

        try:

            with open(

                self.configPath,

                "r",

                encoding="utf-8"

            ) as file:

                self.config = json.load(file)

        except FileNotFoundError:

            self.config = self.DEFAULT_CONFIG.copy()

            self.save()

        except json.JSONDecodeError:

            self.config = self.DEFAULT_CONFIG.copy()

            self.save()

    # -----------------------------------------------------

    def save(self):
        """
        Save configuration to JSON.
        """

        with open(

            self.configPath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.config,

                file,

                indent=4

            )

    # -----------------------------------------------------

    def get(

        self,

        key,

        default=None

    ):
        """
        Return configuration value.
        """

        return self.config.get(

            key,

            default

        )

    # -----------------------------------------------------

    def set(

        self,

        key,

        value

    ):
        """
        Update configuration value.
        """

        self.config[key] = value

    # -----------------------------------------------------

    def update(self):
        """
        Save current configuration.
        """

        self.save()

    # -----------------------------------------------------

    def reset(self):
        """
        Restore default configuration.
        """

        self.config = self.DEFAULT_CONFIG.copy()

        self.save()

    # -----------------------------------------------------

    def all(self):
        """
        Return complete configuration.
        """

        return self.config