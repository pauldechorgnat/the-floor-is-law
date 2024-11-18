from doccano_client import DoccanoClient
from dotenv import load_dotenv
import os

load_dotenv()


USERNAME = os.environ.get("ADMIN_USERNAME")
PASSWORD = os.environ.get("ADMIN_PASSWORD")

PROJECT_NAME = os.environ.get("PROJECT_NAME")

client = DoccanoClient(base_url="http://localhost:8000")
client.login(
    username=USERNAME,
    password=PASSWORD,
)

projects = list(filter(lambda x: x.name == PROJECT_NAME, client.list_projects()))

if len(projects) > 0:
    project_id = projects[0].id
    print("Project already exists")
else:
    print("Creating project")

    response = client.create_project(
        name=PROJECT_NAME,
        description="Annotation de textes de lois dans des décisions de justice",
        project_type="SequenceLabeling",
        allow_overlapping=False,
    )

    project_id = response.id

    response = client.create_label_type(
        project_id=project_id,
        type="span",
        text="article",
        color="#FFDF00",
    )

    print(response)
