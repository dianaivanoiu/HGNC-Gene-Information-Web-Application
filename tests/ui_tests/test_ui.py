import pytest
from pathlib import Path

from HGNCapp import app
from HGNCapp import settings

# ------------------------------------------------------------------
# app tests
# ------------------------------------------------------------------

def test_create_app_data_file_error(tmp_path, monkeypatch):
    """Test that input file exists"""
    missing_file = tmp_path / "does_not_exist.json"
    monkeypatch.setattr(settings, "DATA_FILE", missing_file)

    with pytest.raises(FileNotFoundError):
        app.create_app()

@pytest.fixture
def client(tmp_path: Path):
    """Create a Flask test client for the application"""
    application = app.create_app()
    application.config["TESTING"] = True

    application.config["DATA"] = [
        {
            "hgnc_id": "HGNC:1",
            "symbol": "BRCA1",
            "name": "Breast Cancer Gene 1",
            "prev_symbol": "",
            "prev_name": "",
            "alias_symbol": "",
            "mane_select": "",
        }
    ]

    with application.test_client() as test_client:
        yield test_client

def test_homepage(client):
    """Test homepage returns HTML content"""
    response = client.get("/")

    assert response.status_code == 200
    assert b"HGNC Gene Information" in response.data


def test_search_by_symbol(client):
    """Test submitting a valid gene by symbol returns expected output"""
    response = client.post("/search", data={"gene": "BRCA1"})

    assert response.status_code == 200
    assert b"HGNC:1" in response.data
    assert b"BRCA1" in response.data
    assert b"Breast Cancer Gene 1" in response.data


def test_search_by_hgnc_id(client):
    """Test submitting a valid gene by HGNC ID returns expected output"""
    response = client.post("/search", data={"gene": "HGNC:1"})

    assert response.status_code == 200
    assert b"HGNC:1" in response.data
    assert b"BRCA1" in response.data
    assert b"Breast Cancer Gene 1" in response.data


def test_search_with_no_gene(client):
    """Test submitting empty gene symbol or HGNC ID returns error message"""
    response = client.post("/search", data={"gene": ""})

    assert response.status_code == 200
    assert b"No gene provided" in response.data


def test_search_gene_not_found(client):
    """Test searching for non-existent gene"""
    response = client.post("/search", data={"gene": "TEST"})

    assert response.status_code == 200
    assert b"not found" in response.data


def test_search_missing_data_field(client):
    """Test searchign for a gene missing all required columns"""
    client.application.config["DATA"] = [
        {
            "hgnc_id": "HGNC:1",
            "symbol": "TEST",
            # "name" is deliberately missing
        }
    ]

    response = client.post("/search", data={"gene": "TEST"})

    assert response.status_code == 200
    assert b"missing data field" in response.data
