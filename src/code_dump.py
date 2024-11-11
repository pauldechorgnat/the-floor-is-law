### Comment télécharger des données interactivement


if __name__ == "__main__":
    import json
    import argparse
    import logging
    from dotenv import load_dotenv
    import os

    load_dotenv()

    judilibre_api_key = os.environ.get("JUDILIBRE_API_KEY")
    judilibre_api_url = os.environ.get("JUDILIBRE_API_URL")

    n_decisions = 100
    

    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "-n", "--number",
        help="Number of decisions to download",
        type=int,
        default=100,
    )

    argument_parser.add_argument(
        "-j", "--juridiction",
        help="Juridiction",
        default="cc",
    )

    arguments = argument_parser.parse_args()

    logging.info(
        msg="Downloading {t}"
    )
