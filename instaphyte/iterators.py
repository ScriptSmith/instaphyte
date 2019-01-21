from socialreaper.apis import ApiError
from socialreaper.iterators import Source, Iter, IterError

from instaphyte.api import InstagramAPI


class Instagram(Source):
    def __init__(self):
        super().__init__()

        self.api = InstagramAPI()

    class InstagramIter(Iter):
        def __init__(self, node, function, count, response_key):
            super().__init__()

            self.node = node
            self.function = function
            self.max = count
            self.response_key = response_key
            self.max_id = None

        def get_data(self):
            self.page_count += 1

            try:
                self.response = self.function(self.node, self.max_id)

                page = self.response['graphql'][self.response_key][
                    "edge_" + self.response_key + "_to_media"]
                self.data = page["edges"]
                self.max_id = page["page_info"]["end_cursor"]

                if not self.max_id:
                    raise StopIteration

            except ApiError as e:
                raise IterError(e, vars(self))

    def hashtag(self, tag, count=0):
        return self.InstagramIter(tag, self.api.hashtag, count, "hashtag")

    def location(self, tag, count=0):
        return self.InstagramIter(tag, self.api.location, count, "location")
