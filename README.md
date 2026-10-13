# HGNC-Gene-Information-Web-Application

---

This project is a Flask web application where the user can search for information about human genes published by the HUGO Gene Nomenclature Committee (HUGO) using either a gene symbol (e.g., BRCA1) or an HGNC ID (e.g., HGNC:1101)

## Installation

### 1. Get the project
Clone the repository and move into its directory 

```bash
git clone https://github.com/dianaivanoiu/HGNC-Gene-Information-Web-Application.git
cd HGNC-Gene-Information-Web-Application
```

This project uses a fully controlled and reproducible Conda environment

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 3. Activate the environment

```bash
conda activate HGNCapp
```

### 4. Install the project

```bash
pip install -e .
```

---

## Download the HGNC data

```bash
curl -L "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt" -o data/hgnc_complete_set.txt
```

The source dataset is maintained by HGNC and may be updated over time

---

## Generate the lightweight dataset

The data filtering module reads `data/hgnc_complete_set.txt` and creates `data/lightweight_dataset.json`:

```bash
python -m HGNCapp.data_filtering 
```
If the HGNC source file is updated, run the data filtering command again to regenerate the JSON file

---

## Run the web application

Run Flask:

```bash
python -m HGNCapp.app
```
Open the link shown by Flask in a web browser

The application can be run by searching by gene symbol (e.g.,`BRCA1`) or HGNC ID (e.g.,`HGNC:1101`)

When you are done, use Ctrl+C to stop the server

---

## Run the tests

```bash
python -m pytest
```

### Measure test coverage

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```
The report is created in htmlcov/index.html