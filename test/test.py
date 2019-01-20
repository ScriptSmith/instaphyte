from unittest import TestCase
from instaphyte import Instagram

hashtags = ["beach", "gym", "puppies", "party", "throwback"]
locations = ["1110037669039751", "212988663", "933522", "213385402",
             "228001889"]

smallSize = 30
mediumSize = 300
largeSize = 3000


class Tests(TestCase):
    def setUp(self):
        self.api = Instagram()

    def _test_size(self, endpoints, function, size):
        for endpoint in endpoints:
            posts = []
            for post in function(endpoint, size):
                self.assertIn("id", post["node"])
                posts.append(post)

            self.assertEqual(size, len(posts))

    def test_hashtag_small(self):
        self._test_size(hashtags, self.api.hashtag, smallSize)

    def test_hashtag_medium(self):
        self._test_size(hashtags[:3], self.api.hashtag, mediumSize)

    def test_hashtag_large(self):
        self._test_size(hashtags[:1], self.api.hashtag, largeSize)

    def test_location_small(self):
        self._test_size(locations, self.api.location, smallSize)

    def test_location_medium(self):
        self._test_size(locations[:3], self.api.location, mediumSize)

    def test_location_large(self):
        self._test_size(locations[:1], self.api.location, largeSize)
