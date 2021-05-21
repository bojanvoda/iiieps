from .InvertedIndex import InvertedIndex
from .NonInverted import NonInvertedIndex


class CreateIndex:
    @staticmethod
    def getIndexByType(indexType, inputPath, outputPath, forceRecreate):
        if indexType == "inverted":
            return InvertedIndex(inputPath, outputPath, forceRecreate)
        elif indexType == "non-inverted":
            return NonInvertedIndex(inputPath, outputPath, forceRecreate)
        else:
            raise Exception("Unknown index type")
