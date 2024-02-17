from flask import Flask, render_template, request, jsonify, request
import os
import base64
from io import BytesIO
from PIL import Image
import re
import os
from time import sleep
app = Flask(__name__)


with open("./data/identifiedPerson.txt", 'w') as file:
    file.truncate(0)  # Clear the file


def aireturned():
    while True:
        sleep(1)
        print('looping')
        with open('./data/identifiedPerson.txt', 'r+') as file:
            lines = file.readlines()
            lockStatus = lines[0].strip()

            if lockStatus == '0':
                continue
            elif lockStatus == '1':
                detectedName = lines[1].strip()
                confidence = lines[2].strip()

                lines[0] = '0\n'  # Write 0 instead of inserting at the top
                file.seek(0)
                file.writelines(lines)

                return detectedName, confidence


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
