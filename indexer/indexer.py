import os
import argparse
from prompt_toolkit import PromptSession
from utils import timing
from retrivedoc import DocumentRetrieval
from index import CreateIndex

#tukaj napisemo podatke za indeksiranje, query, pre-procesiranje
@timing
def initIndexer(indexType, inputPath, outputPath, forceRecreate=False):
    index = CreateIndex.getIndexByType(indexType, inputPath, outputPath, forceRecreate)
    timePassed, result = index.buildIndex()
    print(f"[{index.indexerType}] Time required to build the index: {timePassed:.2f} ms")
    return DocumentRetrieval(index)


def search():
    pass


def repl(dr, numResults=20):
    session = PromptSession()
    helpMenu = """help supported commands: 
    - help 
    - max-results <number> - set the maximum number of results, 
    - recreate - recreate current indexer method
    - indexer-type (inverted|non-inverted) - sets the type of the indexer
    - exit - exits the mode
    - anything else performs a search on the chosen index
"""
    print(helpMenu)
    while True:
        try:
            text = session.prompt(f"[{dr.indexer.indexerType}]> Enter query: ")
        except KeyboardInterrupt:
            print("Exit by pressing ctrl+D")
            continue
        except EOFError:
            break
        else:
            if text.startswith("max-results"):
                try:
                    numResults = int(text.split(" ")[1])
                except Exception:
                    print("Try again: `max-results <number>`")
            elif text.startswith("indexer-type"):
                try:
                    dr = initIndexer(text.split(" ")[1], dr.indexer.inputPath, dr.indexer.outputPath, forceRecreate=False)
                except Exception:
                    print("Try again: `indexer-type (inverted|non-inverted)`")
            elif text == "recreate":
                try:
                    dr = initIndexer(dr.indexer.type, dr.indexer.inputPath, dr.indexer.outputPath, forceRecreate=True)
                except Exception:
                    print("Try again: `indexer-type (inverted|non-inverted)`")
            elif text == "exit":
                break
            elif text == "help":
                print(helpMenu)
            else:
                print('Enter your query:', text)
                dr.query(text, numResults=numResults)
    print('exiting')


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The path `{arg}` does not exist!")
    else:
        return arg

# get user arguments:
#   - input and output paths,
#   - operation mode [build, run]
#       - build -> builds the indices
#       - run   -> executes a query on the built indices
#   - [optional] indexer kind [inverse, non-inverted] -> if we are not running the query we do not need this
#   - [optional] user query -> if an index is being built we do not need this
def processArgs():
    parser = argparse.ArgumentParser(description='Inverted index builder and retriever')
    parser.add_argument('-i', '--input', required=True, default='empty',
                        help='[required] Input file', metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', '--output', required=True, default='empty',
                        help='[required] Output file', metavar="FILE")
    parser.add_argument('-m', '--method', required=False, default='inverted',
                        help='[optional] Choose to use to retrieve the index. Available options: (inverted| noninverted), default is inverted.')
    parser.add_argument('--force-recreate', required=False, default=None, action='store_true',
                        help='[optional] Recreated indices.')
    parser.add_argument('--interactive', required=False, default=False, action='store_true',
                        help='[optional] Enable users to enter multiple queries.')
    parser.add_argument('--query', required=False, default=None,
                        help='[optional] execute query (use quotation marks)')
    parser.add_argument('--num-results', required=False, default=20, type=int,
                        help='[optional] User can set number of retrieved results (default=20)')
    return parser.parse_args()


if __name__ == "__main__":
    args = processArgs()
    dr = initIndexer(args.method, args.input, args.output, forceRecreate=args.force_recreate)
    if args.interactive:
        repl(dr, args.num_results)
    elif args.query:
        dr.query(args.query, numResults=args.num_results)
