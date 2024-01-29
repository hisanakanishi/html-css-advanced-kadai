from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from io import BytesIO
import os

img = load_img('c:/Users/hinak/OneDrive/デスクトップ/cat1.png', target_size=(224, 224))
img_array = img_to_array(img)
img_array = img_array.reshape((1, 224, 224, 3))
img_array = preprocess_input(img_array)

model_path = 'd:/vgg16.h5'
model = load_model(model_path)
result = model.predict(img_array)

from tensorflow.keras.applications.vgg16 import decode_predictions
pred_ten = decode_predictions(result)
import pandas as pd
categories = [item[1] for sublist in pred_ten for item in sublist]
probabilities = [item[2] for sublist in pred_ten for item in sublist]

df = pd.DataFrame({'カテゴリ':categories, '確率':probabilities})
prediction = df
print(prediction)