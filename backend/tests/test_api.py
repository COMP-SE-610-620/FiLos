import requests
import unittest

# assuming your FastAPI app is running on localhost:8000
url = 'http://localhost:8000'

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nStarting Test Suite...\n")

    @classmethod
    def tearDownClass(cls):
        print("\nTest Suite Completed.\n")

    def setUp(self):
        print(f"Running test: {self._testMethodName}")

    def test_hello(self):
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "FinGPT")

    def test_chat_text(self):
        response = requests.post(f"{url}/chat/text", data={"text_input": "Hello"})
        self.assertEqual(response.status_code, 200)

    def test_text_to_speech(self):
        response = requests.get(f"{url}/text-to-speech/", params={"text_input": "Hello"})
        self.assertEqual(response.status_code, 200)
    
    def test_chat_speech(self):
    # Open an audio file in binary mode
        with open("output.wav", "rb") as audio_file:
            # Send a POST request to the /chat/speech endpoint with the audio file
            response = requests.post(f"{url}/chat/speech", files={"audio": audio_file})
            # Assert the response
            self.assertEqual(response.status_code, 200)

    

    def tearDown(self):
        print(f"Test: {self._testMethodName} passed.\n")

if __name__ == '__main__':
    unittest.main()