# WIER: Assigment 3, indexing and processing


## Requirements
To run the code you will need to install `Pipenv`:

```git bash
pip install --user pipenv
```

navigate to `./indexer/` and then:
```git bash
cd indexer/
pipenv install
pipenv shell # enters the new environment

```
## Running
After creating new environment, run:
```bash
# to run a query on the reverse index
python indexer.py -i ../input -o ../output --method inverted --query "trgovina"

# re-create the index and perform a single query
python indexer.py -i ../input -o ../output --method inverted --query "trgovina" --force-recreate

# to run a query on the sequential index with maximum of 2 results:
python indexer.py -i ../input -o ../output --method sequential --query "trgovina" --num-results 2

# execute multiple queries
# type `help` to list all the options
python indexer.py -i ../input -o ../output --interactive

# list all possible options
python indexer.py --help

```

If you want to change the input file  `--force-recreate` is provided.

