import os


def isRootUser():

    return os.geteuid() == 0

def checkSystemAccess():
    if isRootUser():
        print("Running with Root User Access")
    else:
        print("Running on Normal User")
        print("Some Cache Area Might Restricted")