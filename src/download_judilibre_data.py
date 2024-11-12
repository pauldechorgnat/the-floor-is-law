import requests

def paginate_results(
    key_id: str,
    total_results: int = 1_000, 
    url: str="",
    **params,
    ):
    
    next_batch = True
    batch_number = 0

    results = []
    n_results = 0

    while next_batch and (n_results < total_results):
        print(n_results)

        params = {
            **params,
            "batch": batch_number,
            "batch_size": 100,
        }

        r = requests.get(
            url=f"{url}/export",
            headers={"KeyId": key_id},
            params=params,            
        )

        r.raise_for_status()

        data = r.json()

        results.extend(data["results"])

        if data.get("next_batch") is None:
            next_batch = False

        n_results = len(results)
        batch_number += 1

    return results[:total_results]


if __name__ == "__main__":
    import json
    import logging
    from dotenv import load_dotenv
    import os
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting ...")

    load_dotenv()

    judilibre_api_key = os.environ.get("JUDILIBRE_API_KEY")
    judilibre_api_url = os.environ.get("JUDILIBRE_API_URL")

    n_decisions = 100
    folder = "./data"


    for jurisdiction in ["cc", "ca", "tj"]:
        filename= os.path.join(folder, f"{jurisdiction}-decisions.json")

        logging.info(
            msg=f"Downloading {n_decisions} from {jurisdiction} into {filename}"
        )

        decisions = paginate_results(
            key_id=judilibre_api_key,
            url=judilibre_api_url,
            total_results=n_decisions,
            jurisdiction=[jurisdiction],
        )


        with open(filename, "w", encoding="utf-8") as file:
            json.dump(decisions, file)

    
