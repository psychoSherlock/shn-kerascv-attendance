
![kerascv](https://github.com/TH-Activities/saturday-hack-night-template/assets/117498997/8a64f118-b69d-4bd7-b59b-a28becafe0dd)



# Facial Registerar :trollface:
This project encompasses a facial recognition system designed for class attendance marking. It consists of three main components: a script using Keras to train a facial recognition model, a data collection script utilizing OpenCV for creating a dataset, and a Flask web application managing student information and attendance. The model training script employs a VGG16-based model, while the data collection script captures faces using Haar Cascade Classifier. The Flask web app, backed by SQLite, includes functionalities for student registry, addition, and real-time attendance marking through captured images. The system runs a continuous loop for face detection and attendance updating until manually interrupted. It is important to ensure the presence of required files, directories, and handle security considerations before execution.

# Team members
1. [Athul Prakash](https://github.com/psychoSherlock)
2. [Sudheesh S Pai](https://github.com/Sudheeshspai)
### Link to product walkthrough
Please play this on VLC or similar players
[https://github.com/psychoSherlock/shn-kerascv-attendance/assets/81918189/91c6bd5b-6c28-46bb-b359-6d85acb0630a](https://github.com/psychoSherlock/shn-kerascv-attendance/assets/81918189/91c6bd5b-6c28-46bb-b359-6d85acb0630a)

## How it Works ?
1. Open CV is used to collect Dataset of Images, using the haarcascade facials.
2. The collected db is fed into Deep learning model that uses imagenet weight, VGG16 transform layers, passes through just one Flatten layer and uses softmax as activation function
3. This data is used by the flask backend to fetch details about the user
4. User can also record new data which will be approved by the admin.
## Libraries used
Keras CV
Open CV
Flask
Flask SQL Alchemy
numpy
Sqlite3
## How to configure
```
git clone https://github.com/psychoSherlock/shn-kerascv-attendance/
cd shn-kerascv-attendance/
virtualenv .env
source .env/bin/activate
pip3 install -r requirements.txt
chmod +x start.sh

```
## How to Run
./start.sh
