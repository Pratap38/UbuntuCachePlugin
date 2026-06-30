from core.utils import bytes_to_mb


class RecommendationEngine:

    def __init__(self):

        self.recommendations = []

    def addRecommendation(

        self,

        title,

        level,

        message

    ):

        self.recommendations.append(

            {

                "title": title,

                "level": level,

                "message": message

            }

        )

    def analyze(self, results):

        self.recommendations.clear()

        for category in results:

            sizeMB = bytes_to_mb(

                category.size

            )

            if category.name == "User Cache":

                self.userCache(sizeMB)

            elif category.name == "APT Cache":

                self.aptCache(sizeMB)

            elif category.name == "Browser Cache":

                self.browserCache(sizeMB)

            elif category.name == "Thumbnail Cache":

                self.thumbnailCache(sizeMB)

            elif category.name == "Temp Files":

                self.tempFiles(sizeMB)

            elif category.name == "Trash":

                self.trash(category.files)

        return self.recommendations

    def userCache(self, size):

        if size > 2048:

            self.addRecommendation(

                "User Cache",

                "Critical",

                "Large User Cache detected. Cleaning strongly recommended."

            )

        elif size > 1024:

            self.addRecommendation(

                "User Cache",

                "Warning",

                "User Cache is moderately large."

            )

    def aptCache(self, size):

        if size > 300:

            self.addRecommendation(

                "APT Cache",

                "Warning",

                "APT Cache is consuming significant storage."

            )

    def browserCache(self, size):

        if size > 500:

            self.addRecommendation(

                "Browser Cache",

                "Warning",

                "Browser Cache unusually large."

            )

    def thumbnailCache(self, size):

        if size < 10:

            self.addRecommendation(

                "Thumbnail Cache",

                "Info",

                "Thumbnail Cache already optimized."

            )

    def tempFiles(self, size):

        if size > 100:

            self.addRecommendation(

                "Temp Files",

                "Warning",

                "Temporary files can be safely removed."

            )

    def trash(self, files):

        if files == 0:

            self.addRecommendation(

                "Trash",

                "Info",

                "Trash is already empty."

            )

        else:

            self.addRecommendation(

                "Trash",

                "Warning",

                f"Trash contains {files} files."

            )