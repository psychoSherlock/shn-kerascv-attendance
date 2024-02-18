from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from glob import glob

IMAGE_SIZE = [224, 224]

train_data_path = 'Dataset/'
valid_data_path = 'Test/'

vgg_model = VGG16(input_shape=IMAGE_SIZE + [3],
                  weights='imagenet', include_top=False)

for layer in vgg_model.layers:
    layer.trainable = False

folders = glob('Dataset/*')

x = Flatten()(vgg_model.output)
prediction = Dense(len(folders), activation='softmax')(x)

model = Model(inputs=vgg_model.input, outputs=prediction)

model.summary()

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

train_data_generator = ImageDataGenerator(rescale=1./255,
                                          shear_range=0.2,
                                          zoom_range=0.2,
                                          horizontal_flip=True)

test_data_generator = ImageDataGenerator(rescale=1./255)

training_set = train_data_generator.flow_from_directory(train_data_path,
                                                        target_size=(224, 224),
                                                        batch_size=32,
                                                        class_mode='categorical')

test_set = test_data_generator.flow_from_directory(valid_data_path,
                                                   target_size=(224, 224),
                                                   batch_size=32,
                                                   class_mode='categorical')

history = model.fit_generator(
    training_set,
    validation_data=test_set,
    epochs=30,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)


model.save('data/keras_model_test.h5')
