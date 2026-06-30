from core.CleaningPreset import CleaningPreset


print(

    "\nAvailable Presets\n"

)

for preset in CleaningPreset.allPreset():

    print(

        preset

    )


print(

    "\nSafe Clean\n"

)

print(

    CleaningPreset.getPreset(

        "Safe Clean"

    )

)


print(

    "\nDeep Clean\n"

)

print(

    CleaningPreset.getPreset(

        "Deep Clean"

    )

)


print(

    "\nBrowser Only\n"

)

print(

    CleaningPreset.getPreset(

        "Browser Only"

    )

)

