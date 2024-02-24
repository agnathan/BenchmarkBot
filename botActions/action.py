import os

CACHE_DIR = "cachedData"


class Action:
    def __init__(self):
        self.name = ""

    def run(self, configs, result):
        pass

    def resultFile(self, dir, filename):
        actionPath = (
            self.__class__.__name__ + "-" + os.path.basename(os.path.splitext(dir)[0])
        )

        return os.path.join(CACHE_DIR, actionPath, filename)
