FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml requirements.txt ./
COPY HGNCapp ./HGNCapp

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir .

RUN mkdir -p data

RUN python -c "from urllib.request import urlretrieve; urlretrieve('https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt', 'data/hgnc_complete_set.txt')"

RUN python -m HGNCapp.data_filtering

EXPOSE 5000

CMD ["python", "-m", "HGNCapp.app"]
