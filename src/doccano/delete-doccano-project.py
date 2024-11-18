from doccano_client import DoccanoClient
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.environ.get("ADMIN_USERNAME")
PASSWORD = os.environ.get("ADMIN_PASSWORD")

PROJECT_NAME = os.environ.get("PROJECT_NAME")

client = DoccanoClient(base_url="http://localhost:8000")
client.login(username=USERNAME, password=PASSWORD,)

projects = list(
    filter(
        lambda x: x.name == PROJECT_NAME,
        client.list_projects()
    )
)

if len(projects) > 0:
    project_id = projects[0].id
    print("Deleting project")
    client.delete_project(project_id=project_id)
else:
    raise ValueError(f"Project named {PROJECT_NAME} does not exist")
