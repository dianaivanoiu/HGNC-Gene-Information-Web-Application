import json

from flask import Flask, request, render_template
from pathlib import Path
import logging
from typing import Dict, Any, Optional, List

from HGNCapp import settings
#from GnomadConstraint.models import model
from HGNCapp.logger import setup_logging


# -------------------------------------------------------------------
# Application Factory
# -------------------------------------------------------------------
def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function encapsulates application creation to avoid
    global side-effects and allow flexible configuration.

    Returns
    -------
    Flask
        Configured Flask application instance.
    """

    # Create Flask instance (NOT at import time anymore)
    app: Flask = Flask(__name__)

    # ---------------------------------------------------------------
    # Logging setup
    # ---------------------------------------------------------------
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Initialising Flask application via factory")

    # ---------------------------------------------------------------
    # Load data (now happens ONCE when app is created)
    # ---------------------------------------------------------------
    DATA_FILE = settings.DATA_FILE

    logger.info(f"Loading data from {DATA_FILE}")

    try:
        # Store data inside app config to avoid global state
        # ✅ This is important for testing and flexibility
        with Path(DATA_FILE).open("r", encoding="utf-8") as file:
            app.config["DATA"] = json.load(file)
            logger.info("Data loaded successfully")

    except Exception:
        logger.exception("Failed to load data")
        raise

    # ---------------------------------------------------------------
    # Routes
    # ---------------------------------------------------------------

    @app.route("/")
    def home() -> str:
        """
        Render the homepage.

        Returns
        -------
        str
            Rendered HTML template.
        """
        logger.debug("Rendering homepage")
        return render_template("index.html")

    @app.route("/search", methods=["POST"])
    def search() -> str:
        """
        Handle gene search requests.

        This endpoint retrieves a gene name from form input
        and queries the dataset loaded at application creation.

        Returns
        -------
        str
            Rendered template containing results or error messages.
        """
        try:
            gene: str = request.form.get("gene", "").strip()
            logger.debug(f"Received search request for gene: {gene}")

            # -------------------------------------------------------
            # Validate input
            # -------------------------------------------------------
            if not gene:
                logger.warning("No gene provided in request")
                return render_template(
                    "index.html",
                    output_text_1="Error: No gene provided",
                    output_text_2=""
                )

            # -------------------------------------------------------
            # Retrieve data from app config (NOT global variable)
            # -------------------------------------------------------
            data: List[Dict[str, str]] = app.config["DATA"]

            selection: Optional[Dict[str, str]] = None
            for entry in data:
                if entry.get("symbol") == gene:
                    logger.info(f"Match found for gene: {gene}")
                    selection = entry

            if selection is None:
                logger.info(f"Gene not found: {gene}")
                return render_template(
                    "index.html",
                    output_text_1=f"Error: Gene '{gene}' not found",
                    output_text_2=""
                )

            logger.info(f"Gene found: {gene}")

            output_text_1: str = f"Found gene:"
            output_text_2: str = (
                f"HGNC ID = {selection['hgnc_id']}, "
                f"Gene symbol = {selection['symbol']}, "
                f"Gene name = {selection['name']}, "
                f"Previous symbol = {selection['prev_symbol']}, "
                f"Previous name = {selection['prev_name']}, "
                f"Alias = {selection['alias_symbol']}, "
                f"MANE Select transcript = {selection['mane_select']}, "
            )

            return render_template(
                "index.html",
                output_text_1=output_text_1,
                output_text_2=output_text_2
            )

        except KeyError as e:
            logger.warning(f"Missing expected data field: {e}")
            return render_template(
                "index.html",
                output_text_1=f"Error: missing data field {str(e)}",
                output_text_2=""
            )

        except Exception as e:
            logger.exception("Unexpected error during search")
            return render_template(
                "index.html",
                output_text_1=f"Error: {str(e)}",
                output_text_2=""
            )

    return app


# -------------------------------------------------------------------
# Application instance (for mounting to gunicorn or mod_wsgi)
# -------------------------------------------------------------------
app: Flask = create_app()


# -------------------------------------------------------------------
# Entry point (local development only)
# -------------------------------------------------------------------
if __name__ == "__main__":
    logging.getLogger(__name__).info("Running Flask app")
    app.run()