# CACHE_PATHS = {
#     "User Cache": "~/.cache",
#     "APT Cache": "/var/cache/apt",
#     "Temp Files": "/tmp",
#     "Logs": "/var/log"
# }



CACHE_CATEGORIES = [

    {
        "name": "User Cache",
        "path": "~/.cache",
        "risk": "Safe"
    },

    {
        "name": "APT Cache",
        "path": "/var/cache/apt",
        "risk": "Safe"
    },

    {
        "name": "Temp Files",
        "path": "/tmp",
        "risk": "Medium"
    },

    {
        "name": "Logs",
        "path": "/var/log",
        "risk": "Medium"
    }
]

SAFE_DELETE_PATHS = [

    "~/.cache",
    "/var/cache/apt",
    "/home/pratap/Desktop/UbuntuCacheCLeaner/tests"
]