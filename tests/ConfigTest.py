from core.ConfigManager import ConfigManager


config = ConfigManager()


print(

    "\nCurrent Configuration\n"

)

print(

    "Default Preset :",

    config.get(

        "defaultPreset"

    )

)

print(

    "Max Threads :",

    config.get(

        "maxThreads"

    )

)

print(

    "Recommendation :",

    config.get(

        "showRecommendation"

    )

)


config.set(

    "maxThreads",

    8

)

config.save()


print(

    "\nUpdated Successfully"

)

print(

    "Max Threads :",

    config.get(

        "maxThreads"

    )

)
