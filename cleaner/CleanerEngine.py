from cleaner.BrowserClean import cleanBrowserCache
from cleaner.Thumbnailcleaner import cleanThumbnailCache
from cleaner.AptCleaner import CleanaptCheck
from cleaner.ThrashCleaner import cleanThrash
# from cleaner.TempCleaner import cleanTempFiles


def cleanUserCache():

    print("User Cache Cleaner Coming Soon")

    return True


cleaners = {

    "User Cache": cleanUserCache,

    "APT Cache": CleanaptCheck,

    # "Temp Files": cleanTempFiles,

    "Browser Cache": cleanBrowserCache,

    "Thumbnail Cache": cleanThumbnailCache,

    "Trash": cleanThrash

}


def cleanSelectedCache(selectedCache):

    results = {}

    for cache in selectedCache:

        cleaner = cleaners.get(cache)

        if cleaner:

            try:

                result = cleaner()

                results[cache] = result

            except Exception as e:

                print(e)

                results[cache] = False

        else:

            results[cache] = False

    return results