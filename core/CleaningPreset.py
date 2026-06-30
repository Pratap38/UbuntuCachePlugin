class CleaningPreset:
    PRESETS = {

        "Safe Clean": [

            "User Cache",

            "Browser Cache",

            "Thumbnail Cache",

            "Trash"

        ],

        "Deep Clean": [

            "User Cache",

            "Browser Cache",

            "Thumbnail Cache",

            "Trash",

            "Temp Files",

            "APT Cache"

        ],

        "Browser Only": [

            "Browser Cache"

        ]

    }
    @classmethod
    def getPreset(cls,PresetName):
        return cls.PRESETS.get(PresetName,[])
    @classmethod
    def allPreset(cls):
        return list(cls.PRESETS.keys())