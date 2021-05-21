from preprocess import Preprocess
from utils import timing


class Index(object):
    def __init__(self, inputPath, outputPath, Recreate=False):
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.Recreate = Recreate
        self.preprocessed = Preprocess.preprocessFiles(self.inputPath, self.outputPath, self.Recreate)
        self.indexerType = "None"
        self.type = "None"

    def buildIndex(self):
        # Builds the index
        pass

    def search(self, query):
        # searches the index
        pass

