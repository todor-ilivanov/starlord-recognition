import re
from google.cloud import vision
import io

class VisionAPI:

    client = None

    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def request(self, path):
        """Detects text in the file."""

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = self.client.text_detection(image=image)

        return response

    # TODO move outside of this class?
    def extract_track_name(self, response):
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        if len(response.text_annotations) == 0:
            return None

        texts = response.text_annotations
        full_text = texts[0].description.split('\n')
        # TODO: make this more robust
        regex = '(It\'s|That one\'s)\s(.+)\sby\s(.+)'
        song = None

        for text in full_text:
            regex_result = re.search(regex, text)
            if regex_result:
                song = regex_result.group(2) + ' ' + regex_result.group(3)
                print("*****Recognized song: " + song)
                break

        return song 