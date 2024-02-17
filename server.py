from flask import Flask, render_template, request, jsonify, request
import os
import base64
from io import BytesIO
from PIL import Image
import re
import os
import time
app = Flask(__name__)


with open("./data/identifiedPerson.txt", 'w') as file:
    file.truncate(0)


def aireturned():
    while True:
        modified_time = os.path.getmtime('./data/identifiedPerson.txt')
        if modified_time != aireturned.last_modified:
            with open('./data/identifiedPerson.txt', 'r') as file:
                lines = file.readlines()
                detectedName = lines[0].strip()
                confidence = lines[1].strip()
                # Do something with detectedName and confidence variables
                return detectedName, confidence
        time.sleep(1)
        aireturned.last_modified = modified_time


aireturned.last_modified = os.path.getmtime('./data/identifiedPerson.txt')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/save', methods=['POST'])
def save_image():
    if 'image/png' in request.get_json()['image']:
        print('Image received')
        image_data = request.get_json()['image']
        image_bytes = base64.b64decode(
            re.search(r'base64,(.*)', image_data).group(1))
        image = Image.open(BytesIO(image_bytes))
        image.save(os.path.join('data', 'capturedImage.png'))

        detectedName, detectedConfidence = aireturned()
        return jsonify({'status': 'success', 'studentName': f'{detectedName}', 'confidence': f'{detectedConfidence}'})
    else:
        print(request.data)
        print('Image not received')
        return jsonify({'status': 'failed'})


if __name__ == '__main__':
    app.run(debug=True)
