from django.shortcuts import render
from .forms import ImageUploadForm
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from io import BytesIO
import os
import pandas as pd

def predict(request):
    if request.method == 'GET':
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        #POSTリクエストによるアクセス時の処理を記述
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            #４章で、画像ファイル(img_file)の前処理を追加
            img_file = BytesIO(img_file.read())
            img = load_img(img_file, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = img_array.reshape((1, 224, 224, 3))
            img_array = preprocess_input(img_array)
            #４章で、判定結果のロジックを追加
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'vgg16.h5')
            model = load_model(model_path)
            result = model.predict(img_array)
            from tensorflow.keras.applications.vgg16 import decode_predictions
            pred_1 = decode_predictions(result)
            categories = [item[1] for sublist in pred_1 for item in sublist]
            probabilities = [item[2] for sublist in pred_1 for item in sublist]
            
            df = pd.DataFrame({'カテゴリ': categories, '確率': probabilities})
            prediction = df.values.tolist()
            img_data = request.POST.get('img_data')
            print(img_data)
            return render(request, 'home.html', {'form': form, 'prediction': prediction, 'img_data': img_data})
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})
