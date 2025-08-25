from keras import Model
from keras.src.applications.mobilenet_v2 import MobileNetV2
from keras.src.layers import Dense
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping


train_dir = 'E:\\AIWork\\Data\\테스트\\'
# rabbit_train_dir = './train/rabbit'
# raccoon_train_dir = './train/raccoon'
# squirrel_train_dir = './train/squirrel'

train_datagen = ImageDataGenerator(
    rescale=1. / 255.0,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=8,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=8,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)


# 모델 불러오기 (사전 학습된 가중치 사용. 최사위 레이어 제거)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(150, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# 기본모델의 레이어 고정 (학습되지 않도록 설정)
for layer in base_model.layers:
    layer.trainable = False

earlyStopping = EarlyStopping(monitor="val_loss", patience=10, verbose=1)

model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_generator,
          epochs=100,
          validation_data=validation_generator,
          steps_per_epoch=train_generator.samples // 8,  # // train_generator.batch_size,
          validation_steps=validation_generator.samples// 8,  # // validation_generator.batch_size
          callbacks=[earlyStopping]
          )

model.save('korean_food_classifier.keras')
