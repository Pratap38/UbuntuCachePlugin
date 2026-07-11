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

    def analyze(

        self,

        results

    ):

        self.recommendations.clear()

        for category in results:

            sizeMB = bytes_to_mb(

                category.size

            )

            if category.name == "User Cache":

                self.checkUserCache(

                    sizeMB

                )

            elif category.name == "APT Cache":

                self.checkAPTCache(

                    sizeMB

                )

            elif category.name == "Browser Cache":

                self.checkBrowserCache(

                    sizeMB

                )

            elif category.name == "Thumbnail Cache":

                self.checkThumbnailCache(

                    sizeMB

                )

            elif category.name == "Temp Files":

                self.checkTempFiles(

                    sizeMB

                )

            elif category.name == "Trash":

                self.checkTrash(

                    category.files

                )

        return self.recommendations

    def checkUserCache(

        self,

        size

    ):

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

    def checkAPTCache(

        self,

        size

    ):

        if size > 300:

            self.addRecommendation(

                "APT Cache",

                "Warning",

                "APT Cache is consuming significant storage."

            )

    def checkBrowserCache(

        self,

        size

    ):

        if size > 500:

            self.addRecommendation(

                "Browser Cache",

                "Warning",

                "Browser Cache unusually large."

            )

    def checkThumbnailCache(

        self,

        size

    ):

        if size < 10:

            self.addRecommendation(

                "Thumbnail Cache",

                "Info",

                "Thumbnail Cache already optimized."

            )

    def checkTempFiles(

        self,

        size

    ):

        if size > 100:

            self.addRecommendation(

                "Temp Files",

                "Warning",

                "Temporary files can be safely removed."

            )

    def checkTrash(

        self,

        files

    ):

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