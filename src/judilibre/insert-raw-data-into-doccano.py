import zipfile
import json
import os
import hashlib
from tqdm import tqdm
from doccano_client import DoccanoClient
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get("ADMIN_USERNAME")
PASSWORD = os.environ.get("ADMIN_PASSWORD")
PROJECT_NAME = os.environ.get("PROJECT_NAME")


client = DoccanoClient(base_url="http://localhost:8000")
client.login(username=USERNAME, password=PASSWORD)

projects = list(filter(lambda x: x.name == PROJECT_NAME, client.list_projects()))

if len(projects) == 0:
    raise ValueError(f"No such project named '{PROJECT_NAME}'")

project_id = projects[0].id


print("Downloading data from doccano to upload differences")

TMP_FOLDER = os.path.join(os.path.dirname(__file__), "tmp")

if not os.path.exists(TMP_FOLDER):
    os.mkdir(TMP_FOLDER)

response = client.download(
    project_id=project_id,
    format="JSONL",
    dir_name=TMP_FOLDER,
)


DOWNLOAD_ZIP = os.path.join(TMP_FOLDER, os.listdir(TMP_FOLDER)[0])

with zipfile.ZipFile(DOWNLOAD_ZIP, "r") as z:
    z.extractall(TMP_FOLDER)

DOWNLOAD_FILE = os.path.join(
    TMP_FOLDER,
    [f for f in os.listdir(TMP_FOLDER) if ".jsonl" in f][0],
)

with open(DOWNLOAD_FILE, "r", encoding="utf-8") as file:
    downloaded_decisions = [json.loads(line) for line in file if len(line) > 1]

downloaded_decisions = {
    f"{d.get('id')}_{d.get('checksum')}": d for d in downloaded_decisions
}

# response = client.upload(
#     project_id=project_id,
#     file_paths=[file_name],
#     task="SequenceLabeling",
#     format="JSONL",
#     column_label="labels",
# )


DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RAW_DATA_FOLDER = os.path.join(DATA_FOLDER, "raw")
INPUT_DATA_FOLDER = os.path.join(DATA_FOLDER, "input")

decisions = []

for f in os.listdir(RAW_DATA_FOLDER):
    with open(os.path.join(RAW_DATA_FOLDER, f), "r", encoding="utf-8") as file:
        decisions.extend(json.load(file))

files_to_upload = []


for d in tqdm(decisions):
    decision_id = d["id"]
    text = d["text"]
    checksum = hashlib.md5(text.encode("utf-8")).hexdigest()
    filename = os.path.join(TMP_FOLDER, f"{decision_id}.jsonl")

    if f"{decision_id}_{checksum}" not in downloaded_decisions:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "id": decision_id,
                    "text": text,
                    "checksum": checksum,
                    "labels": [],
                },
                file,
            )
        files_to_upload.append(filename)


response = client.upload(
    project_id=project_id,
    task="SequenceLabeling",
    column_label="labels",
    format="JSONL",
    file_paths=files_to_upload,
)

print(f"{len(files_to_upload)} file(s) inserted into Doccano")


for f in os.listdir(TMP_FOLDER):
    os.remove(os.path.join(TMP_FOLDER, f))

os.rmdir(TMP_FOLDER)
