import os
import pickle
import cv2 as cv
import numpy as np
from sklearn.preprocessing import LabelEncoder


def pred_output(pred_list,feature):
    current_path = os.path.dirname(os.path.abspath(__file__))
    model_name = ['_lightgbm','_linear','_logistic','_svr','_xgboost']
    pred =[]
    for i in range (len(pred_list)):
        for j in range(len(model_name)):
            weight_path = os.path.join(current_path,'result',pred_list[i]+model_name[j]+'.pickle.dat')
            with open(weight_path, 'rb') as file:
                loaded_model_and_data = pickle.load(file)
            model = loaded_model_and_data['model']
            new_feature = np.delete(feature, loaded_model_and_data['split_key'])
            if model_name[j] == '_linear' or  model_name[j] == '_logistic'or  model_name[j] == '_svr':
                ss = loaded_model_and_data['ss']
                new_feature = ss.transform([new_feature])[0]
            predict = model.predict([new_feature])
            if model_name[j] == '_logistic':
                encoder = loaded_model_and_data['encoder']
                predict = encoder.inverse_transform(predict)
            pred.append(round(float(predict[0]),3))
    
    return pred
       

