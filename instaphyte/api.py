import json
from time import sleep

from socialreaper.apis import API


class InstagramAPI(API):
    def __init__(self):
        super().__init__()

        self.url = "https://instagram.com/explore"

        # Work better with poor connections
        self.retry_rate = 10
        self.num_retries = 15

    def api_call(self, edge, parameters, return_results=True):
        req = self.get("%s/%s" % (self.url, edge), params=parameters,
                       headers={'Connection': 'close'})

        if not req:
            return None

        if return_results:
            try:
                return req.json()
            except json.JSONDecodeError:
                print("API response was not valid JSON")
                print(req.text)
                sleep(10)
                return self.api_call(edge, parameters, return_results=return_results)

    def hashtag(self, tag, max_id=None, params=None):
        parameters = {
            "__a": 1,
            "max_id": max_id
        }
        parameters = self.merge_params(parameters, params)

        return self.api_call("tags/" + tag, parameters)

    def location(self, location, max_id=None, params=None):
        parameters = {
            "__a": 1,
            "max_id": max_id
        }
        parameters = self.merge_params(parameters, params)

        return self.api_call("locations/" + location, parameters)
