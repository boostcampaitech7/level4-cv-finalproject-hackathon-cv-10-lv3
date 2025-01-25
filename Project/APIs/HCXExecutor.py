import requests
import json

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

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