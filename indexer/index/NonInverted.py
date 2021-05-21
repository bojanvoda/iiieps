from utils import timing, timed
from .index import Index


@timed
def search(self, query):
    results = []
    for documentName in self.preprocessed:
        indices = [str(i) for i, x in enumerate(self.preprocessed[documentName]["content"]) if x in query]
        if len(indices) > 0:
            results.append((documentName, len(indices), ",".join(indices)))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


class NonInvertedIndex(Index):
    def __init__(self, inputPath, outputPath, Recreate):
        super(NonInvertedIndex, self).__init__(inputPath, outputPath, Recreate)
        self.indexerType = "non-inverted"
        self.type = "non-inverted"

    @timed
    def buildIndex(self):
        pass
