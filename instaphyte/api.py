from time import time, sleep

from socialreaper.apis import API


class InstagramAPI(API):
    def __init__(self):
        super().__init__()

        self.url = "https://instagram.com/explore"
        self.request_rate = 0
        self.last_request = time()

    def api_call(self, edge, parameters, return_results=True):
        req = self.get("%s/%s" % (self.url, edge), params=parameters,
                       headers={'Connection': 'close'})

        time_diff = time() - self.last_request
        if time_diff < self.request_rate:
            sleep(time_diff)

        self.last_request = time()

        if not req:
            return None

        if return_results:
            return req.json()

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
