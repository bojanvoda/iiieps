from preprocess import Preprocess
import texttable as tt
import random
from utils import timing


class DocumentRetrieval:
    def __init__(self, indexer):
        self.indexer = indexer

    def __printResults(self, Putresult, numResults = 20):
        preprocessed = self.indexer.preprocessed
        procesirani = 0
        table = tt.Texttable()
        table.header(["Rank", "Frequency", "Document"])
        table.set_cols_width([10, 20, 40, 100])
        table.set_cols_dtype(["i", "i", "t", "t"])
        for result in Putresult:
            if procesirani >= numResults:
                break
            documentName = result[0]
            frequency = result[1]
            indices = sorted([int(x) for x in result[2].split(",")])
            content = preprocessed[documentName]["content"]
            for i in range(min(5, len(indices))):
                idx = indices[i]
            table.add_row((procesirani + 1, frequency, documentName))
            procesirani = procesirani + 1
        if procesirani > 0:
            print(table.draw())
        else:
            print("Ni rezultate")

    def query(self, userQuery, numResults=15):
        timePassed, resultSet = self.indexer.search(Preprocess.tokenize(userQuery))
        print(f"[{self.indexer.indexerType}] Found {len(resultSet)} results in {timePassed:.2f} ms")
        self.__printResults(resultSet, numResults=numResults)
        return resultSet

    def randomTokens(self):
        preprocessed = self.indexer.preprocessed
        file = random.choice(list(preprocessed.keys()))
        return " ".join(random.sample(preprocessed[file]["tokens"], random.randint(2, 5)))