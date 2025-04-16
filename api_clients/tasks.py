from api_clients.base_client import BaseAPIClient
from utils.helpers import CLICKUP_HEADERS

class TasksClient(BaseAPIClient):
    def __init__(self, base_url, headers=CLICKUP_HEADERS):
        super().__init__(base_url, headers)

    def create_task(self, list_id, payload):
        return self.post(f"/list/{list_id}/task", json=payload)

    def get_tasks(self, list_id):
        return self.get(f"/list/{list_id}/task")

    def update_task(self, task_id, payload):
        return self.put(f"/task/{task_id}", json=payload)

    def delete_task(self, task_id):
        return self.delete(f"/task/{task_id}")
    
    def get_first_workspace_id(self):
        return self.get(f"/team")
    
    def get_first_list_id(self):

        workspace_resp = self.get("/team")
        workspace_id = workspace_resp.json()["teams"][0]["id"]

        space_resp = self.get(f"/team/{workspace_id}/space")
        space_id = space_resp.json()["spaces"][0]["id"]

        folder_resp = self.get(f"/space/{space_id}/folder")
        folder_id = folder_resp.json()["folders"][0]["id"]

        list_resp = self.get(f"/folder/{folder_id}/list")
        list_id = list_resp.json()["lists"][0]["id"]

        return list_id
