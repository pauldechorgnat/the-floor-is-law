from doccano_client import DoccanoClient
from dotenv import load_dotenv
import datetime
import os
import json
import zipfile

load_dotenv()

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "data")
ANNOTATED_DATA_FOLDER = os.path.join(DATA_FOLDER, "annotated")

USERNAME = os.environ.get("ADMIN_USERNAME")
PASSWORD = os.environ.get("ADMIN_PASSWORD")

PROJECT_NAME = os.environ.get("PROJECT_NAME")

client = DoccanoClient(base_url="http://localhost:8000")
client.login(
    username=USERNAME,
    password=PASSWORD,
)

projects = list(filter(lambda x: x.name == PROJECT_NAME, client.list_projects()))

if len(projects) == 0:
    raise ValueError(f"Project named {PROJECT_NAME} does not exist")

project_id = projects[0].id

response = client.list_download_options(project_id=project_id)
path_to_zipfile = client.download(
    project_id=project_id,
    format="JSONL",
    only_approved=True,
    dir_name=ANNOTATED_DATA_FOLDER,
)


with open(
    os.path.join(ANNOTATED_DATA_FOLDER, "annotated_data.json"),
    "r",
    encoding="utf-8",
) as file:
    annotated_data = json.load(file)


with zipfile.ZipFile(path_to_zipfile, "r") as z:
    z.extractall(ANNOTATED_DATA_FOLDER)

with open(os.path.join(ANNOTATED_DATA_FOLDER, "admin.jsonl")) as file:
    new_annotated_data = [json.loads(line) for line in file if len(line) > 1]

new_annotated_data = [
    {
        "id": d["id"],
        "checksum": d["checksum"],
        "label": d.get("label", []),
        "timestamp": str(datetime.datetime.now()),
    }
    for d in new_annotated_data
]

annotated_data += new_annotated_data

with open(
    os.path.join(ANNOTATED_DATA_FOLDER, "annotated_data.json"), "w", encoding="utf-8"
) as file:
    json.dump(
        annotated_data,
        file,
        indent=4,
    )

os.remove(os.path.join(ANNOTATED_DATA_FOLDER, "admin.jsonl"))
os.remove(path_to_zipfile)
