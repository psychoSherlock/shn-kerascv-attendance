from flask import Flask, render_template, request, jsonify, request
import os
import base64
from io import BytesIO
from PIL import Image
import re
import os
from time import sleep
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///class.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    attendance = db.Column(db.Boolean)

    def __init__(self, id, name, attendance):
        self.id = id
        self.name = name
        self.attendance = attendance


# Create the student table
with app.app_context():
    db.create_all()


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


def get_student_details(student_id):
    with app.app_context():
        student = Student.query.filter_by(id=student_id).first()
        if student:
            return {
                'id': student.id,
                'name': student.name,
                'attendance': student.attendance
            }
        else:
            return None


def markAttendance(student_id):
    with app.app_context():
        student = Student.query.filter_by(id=student_id).first()
        if student:
            student.attendance = True
            db.session.commit()
            return True
        else:
            return False


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
        detectedStudentId, detectedConfidence = aireturned()
        markAttendance(detectedStudentId)
        return jsonify({'status': 'success', 'studentName': f'{get_student_details(detectedStudentId)["name"]}', 'attendance': 'Marked', 'confidence': f'{detectedConfidence}'})
    else:
        print(request.data)
        print('Image not received')
        return jsonify({'status': 'failed'})


if __name__ == '__main__':
    app.run(debug=True)
