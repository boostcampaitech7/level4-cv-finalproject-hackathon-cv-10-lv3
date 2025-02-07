import requests
import json
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)

    
HOST = config["HCX_host"]
API_KEY = config["HCX_api_key"]
REQUEST_ID = config["HCX_request_id"]


class CompletionExecutor:
    def __init__(self):
        self._host = HOST
        self._api_key = API_KEY
        self._request_id = REQUEST_ID

    def execute(self, completion_request):
        headers = {
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        content = None
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            wrt = False
            for line in r.iter_lines():
                if line:
                    message = line.decode("utf-8")
                    print(message)

                    if message.startswith('event:result'):
                        wrt = True
                    elif wrt:
                        try:
                            if message.startswith('data:'):
                                data = json.loads(message[5:])
                                content = data["message"]["content"]
                                wrt = False
                        except json.JSONDecodeError as e:
                            print(f"Error parsing message: {e}")
                        except KeyError as e:
                            print(f"Missing key in message: {e}")

        return content