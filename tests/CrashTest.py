from core.CrashLogger import CrashLogger


try:

    x = 10 / 0

except Exception as e:

    CrashLogger.log(

        e

    )

print(

    "Crash Logged Successfully."

)