import os
import requests

pat = "ed90df12d9d28f036e244d3505785a66dc9214ac"
repo = "eedorenko/kubemlops"


class GhActionsClient:

    def __init__(self, repo, pat):
        self.owner, self.repo = repo.split("/")
        self.personal_access_token = pat

        self.base_url = f'https://api.github.com/repos/{self.owner}/{self.repo}'
        self.headers = {'authorization': f'token {self.personal_access_token}',
                   'accept': 'application/vnd.github.everest-preview+json'}

    def send_dispatch_event(self, event_type, client_payload):
        url = self.base_url + "/dispatches"        
        data = {'event_type': event_type, 'client_payload': client_payload}
        response = requests.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 204
        print(response)

    def add_comment(self, pr_num, comment):
        url = self.base_url + "/issues/{pr_num}/comments".format(pr_num=pr_num)        
        data = {'body': comment}
        response = requests.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 201
        print(response)

    def add_labels(self, pr_num, labels):
        url = self.base_url + "/issues/{pr_num}/labels".format(pr_num=pr_num)        
        data = {'labels': labels}
        response = requests.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 200
        print(response)

        
def get_gh_actions_client():
    return GhActionsClient(os.getenv("GITHUB_REPOSITORY"), os.getenv("GITHUB_TOKEN"))

if __name__ == "__main__":
    client = GhActionsClient(repo, pat)
    #payload = {'sha': sha, 'pr_num': pr_num}
    #client.send_dispatch_event(sha="", pr_num="1", phase="Model is registered")
    #client.add_comment(pr_num="1", comment="Hello from Client")
    #client.add_labels(pr_num="6", labels=["model registered"])



