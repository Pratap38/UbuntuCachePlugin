from core.utils import bytes_to_mb


class RecommendationEngine:

    def __init__(self):

        self.recommendations = []

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

            self.recommendations.append(

                "Large User Cache detected. Cleaning recommended."

            )

        elif size > 1024:

            self.recommendations.append(

                "User Cache is moderately large."

            )

    def aptCache(self, size):

        if size > 300:

            self.recommendations.append(

                "APT Cache is consuming significant storage."

            )

    def browserCache(self, size):

        if size > 500:

            self.recommendations.append(

                "Browser Cache unusually large."

            )

    def thumbnailCache(self, size):

        if size < 10:

            self.recommendations.append(

                "Thumbnail Cache already optimized."

            )

    def tempFiles(self, size):

        if size > 100:

            self.recommendations.append(

                "Temporary files can be safely removed."

            )

    def trash(self, files):

        if files == 0:

            self.recommendations.append(

                "Trash is already empty."

            )

        else:

            self.recommendations.append(

                f"Trash contains {files} files."

            )