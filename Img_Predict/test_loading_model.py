import pickle
import cv2 as cv
import numpy as np
from glcm import get_gray_level_feature


model_name = 'result/melt-model/tensile_xgboost.pickle.dat'
with open(model_name, 'rb') as file:
    loaded_model_and_data = pickle.load(file)
image_path = 'data/ct-example/item01/01.jpg'
img = cv.imread(image_path)
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

feature = get_gray_level_feature(img)

parm = [1,1,1,1,1]  #製成參數

features = np.array(np.concatenate([feature, parm]))

loaded_model = loaded_model_and_data['model']
loaded_split_key = loaded_model_and_data['split_key']



new_feature = np.delete(features, loaded_split_key)

predict = loaded_model.predict([new_feature])
print(predict)