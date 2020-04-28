import os
import json
from gh_actions_client import get_gh_actions_client


class DispatchEventHandler:

    MODEL_REGISTRATION_COMMENT = "Model **{model_name}** has been registered \
                                  at the [Model Registry ](http://microsoft.com) \
                                  with the following metrics **{metrics}**"
    MODEL_REGISTRATION_LABEL = "Model Registered"                                  

    def __init__(self):
        event_payload_file = os.getenv('GITHUB_EVENT_PATH')
        with open(event_payload_file, 'r') as f:
            raw_payload = json.load(f)
        
            print("Payload")
            print(raw_payload)
            
            self.event_type = raw_payload['action']    
            print(f'::set-output name=EVENT_TYPE::{self.event_type}')

            if ('client_payload' in raw_payload):
                self.event_client_payload = raw_payload['client_payload']
                
                if ('pr_num' in self.event_client_payload):
                    self.pr_num = self.event_client_payload['pr_num']            
                if ('sha' in self.event_client_payload):
                    self.sha = self.event_client_payload['sha']            
                
                print(f'::set-output name=SHA::{self.sha}')
                print(f'::set-output name=ISSUE_NUMBER::{self.pr_num}')

            else:
                self.event_client_payload = None

    def add_comment(self, comment):        
        get_gh_actions_client().add_comment(self.pr_num, comment)

    def add_label(self, label):        
        get_gh_actions_client().add_labels(self.pr_num, [label])

    def fire_event(self, event):        
        get_gh_actions_client().send_dispatch_event(self.sha, self.pr_num, event)

    # TODO: Fetch params from MLFlow
    def get_model_params(self):
        return {'model_name': 'Mexican Food', 
                'metrics': 'Spicy level:10.0'}

 
    def dispatch(self):
        model_params = self.get_model_params() 
        comment = self.MODEL_REGISTRATION_COMMENT.format(model_name=model_params['model_name'],
                                                  metrics=model_params['metrics'])
        self.add_comment(comment)
        self.add_label(self.MODEL_REGISTRATION_LABEL)


if __name__ == "__main__":
    event_dispatcher = DispatchEventHandler()
    event_dispatcher.dispatch() 