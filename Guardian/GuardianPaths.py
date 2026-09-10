from pathlib import Path


class GuardianPaths:

    APP_NAME = "ubuntu-cache-cleaner"

    @classmethod        ##we are been adding  class method in order to restirct to copy of own object
    def homeDirectory(cls) -> Path:
        return Path.home()

    @classmethod
    def configDirectory(cls) -> Path:
        return (
            cls.homeDirectory()
            / ".config"
            / cls.APP_NAME
        )

    @classmethod
    def configFile(cls) -> Path:
        return (
            cls.configDirectory()
            / "guardian_config.json"
        )

    @classmethod
    def stateDirectory(cls) -> Path:
        return (
            cls.homeDirectory()
            / ".local"
            / "state"
            / cls.APP_NAME
        )

    @classmethod
    def stateFile(cls) -> Path:
        return (
            cls.stateDirectory()
            / "guardian_state.json"
        )

    @classmethod
    def logDirectory(cls) -> Path:
        return (
            cls.stateDirectory()
            / "logs"
        )

    @classmethod
    def logFile(cls) -> Path:
        return (
            cls.logDirectory()
            / "guardian.log"
        )