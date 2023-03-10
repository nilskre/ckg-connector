# ckg-connector

The goal of this project is to easily transform various datasets into suitable input files for the [Clinical Knowledge Graph (CKG)](https://github.com/MannLabs/CKG).
This project was created during a practical in the [Database Systems Reseach group from Prof. Gertz at Heidelberg University](https://dbs.ifi.uni-heidelberg.de/).

Student: Nils Krehl  
Supervisor: Prof. Dr. Gertz  
Semester: Winter semester 2022/23

## Features
- **Open Closed principle**: Only one custom dataset class needs to be added, to add a new dataset. All other project files do not need to be adapted.
- **Generate mapping from ICD to DOID** (Disorder Ontology, used by the CKG)
- **Transformation ICD to DOID**
- **Transformation OPS to Snomed CT**
- **Transformation of manually defined mappings**
- **Mapping and Transformation statistics**
- **Generate CKG input files** (with DOID, Snomed CT and manually defined mappings)

## Setup

For using this project a Python environment with the necessary packages is required. The easiest way is to install [Poetry](https://python-poetry.org/) and then run ```poetry install``` in the project root directory. For details how to use poetry see [here](https://github.com/nilskre/ckg-connector#environment).

## Usage

### Setting

Given some dataset file, the goal is to map the data into the CKG. Therefore the dataset needs to be transformed into input files suitable for the CKG.

An example dataset could look like this:

| Patient ID | ICD_A00 | ICD_A01 | OPS_1-100 | OPS_2-200 | Some clinical param |
|------------|:-------:|--------:|:---------:|:---------:|:-------------------:|
| 1          |    0    |       1 |     0     |     1     |         0.1         |
| 2          |    1    |       1 |     1     |     0     |         0.2         |

Instead of coding all transformations repeately, it is only necessary to create a custom dataset class, which returns the dataset in a standardized way. All subsequent steps are then based on this standardized representation and do not need to be adapted.
The whole pipeline looks like this:  
dataset -> **custom dataset class** -> standardized intermediate form -> build mappings -> transform dataset -> CKG input files 

### Workflow

1. **Create own custom dataset class**, which inherits from [dataset.py](./ckg_connector/dataset/dataset.py) and implements the abstract methods. As an example, see [synthetic_dataset.py](./ckg_connector/dataset/synthetic_dataset.py).
2. Create data folder: The structure of the data folder should look like this:
   - input: Contains the dataset. Here you need to **insert your dataset file**.
   - mappings: Contains the mappings and the mapping statistics. The mappings are downloaded or built automatically. If you want to specifiy **custom mappings** you can put them in a file called manual.csv. You can use the [manual_template.csv](./ckg_connector/data/mappings/manual_template.csv) as a template.
   - ontologies: Here the downloaded ontologies are stored. The ontologies are downloaded automatically.
   - output: Here the CKG output files are stored (clinical_data.csv). As well as the statistics of the transformation process.
   - templates: Contains the templates for the CKG input files.

[![data folder structure](./docs/structure_data_folder.png)](./docs/structure_data_folder.png)

3. Run the project:
   - If your data folder is located in [./data](./data): ```python ckg_connector/main.py```
   - If your data folder is located elsewhere: ```python ckg_connector/main.py --datadir <absolute path to the data folder>```

## Development

### Environment

For Python packaging and dependency management [Poetry](https://python-poetry.org/) is used. The [installation docs](https://python-poetry.org/docs/#installation) describe how to install Poetry.

Helpful commands:
- Add new dependencies: ```poetry add <dependency>```
- Update lock file (after adding new dependencies in pyproject.toml): ```poetry lock```
- Install dependencies from lock file: ```poetry install```
- Update dependencies to newest version: ```poetry update```
- Open shell with this environment: ```poetry shell```

### Testing

- Run all unit tests: ```python -m unittest discover```
- For measuring test coverage run: ```coverage run -m unittest discover``` and ```coverage report```. To view an html version with the code coverage run ```coverage html``` and open the file ```htmlcov/index.html```.

### Code quality

#### Tools
For ensuring code quality following tools are used:
- [isort](https://isort.readthedocs.io/en/latest/) for sorting imports
- [black](https://black.readthedocs.io/en/stable/) for automated code formatting
- [flake8](https://flake8.pycqa.org/en/latest/) for code linting and checking compliance with PEP8

#### Pre-commit hooks

To ensure that the code is formatted and linted correctly, pre-commit hooks are used. They are defined in [.pre-commit-config.yaml](./.pre-commit-config.yaml). To install the hooks run ```pre-commit install```. The hooks are then executed before each commit.
For running the hook for all project files (not only the changed ones) run ```pre-commit run --all-files```.
