import unittest
import events_predictor

class TestEventsPredictor(unittest.TestCase):

    def test_replace_params(self):
        prompt = "Hello [[name]]"
        params = {"[[name]]": "world"}
        self.assertEqual(events_predictor.replace_params(prompt, params), "Hello world")


if __name__ == '__main__':
    unittest.main()