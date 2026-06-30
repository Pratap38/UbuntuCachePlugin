from core.utils import format_size


class CleanupEstimator:

    def estimate(

        self,

        results

    ):

        totalFiles = 0

        totalSize = 0

        for category in results:

            totalFiles += category.files

            totalSize += category.size

        estimatedTime = max(

            1,

            totalFiles // 1000

        )

        return {

            "files": totalFiles,

            "size": format_size(

                totalSize

            ),

            "seconds": estimatedTime

        }