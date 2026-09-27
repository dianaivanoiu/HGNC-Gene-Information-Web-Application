# HGNC-Gene-Information-Web-Application

---

# Installation

This project uses a fully controlled and reproducible Conda environment.

## 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

## 2. Activate the environment

```bash
conda activate HGNCapp
```

## 3. Install the project

```bash
pip install -e .
```

The editable installation allows changes made to the source code to be immediately reflected without reinstalling the package.

---

# Download the HGNC data

```bash
curl -L "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt" -o data/hgnc_complete_set.txt
```