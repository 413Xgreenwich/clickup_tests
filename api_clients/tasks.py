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