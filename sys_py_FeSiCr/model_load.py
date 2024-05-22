# @file    model.py
# @author  Kuan-Di Jiang
# @brief   loading AI model (abandon file)

import xgboost as xgb
import lightgbm as lgb
import catboost as cat
import os
import sys
import joblib
import logging
logging.basicConfig(level=logging.INFO)
sys.path.append('.')
current_path = os.path.dirname(os.path.abspath(__file__))
folder_xgb = 'model_set_FeSiCr/xgb'
folder_cat = 'model_set_FeSiCr/cat'
folder_lgb = 'model_set_FeSiCr/lgb'



## model declaration (xgb)
model_mu_xgb_50 = xgb.XGBRegressor()
model_mu_xgb_200 = xgb.XGBRegressor()
model_mu_xgb_400 = xgb.XGBRegressor()
model_mu_xgb_800 = xgb.XGBRegressor()
model_Pcv_xgb_50 = xgb.XGBRegressor()
model_Pcv_xgb_200 = xgb.XGBRegressor()
model_Pcv_xgb_400 = xgb.XGBRegressor()
model_Pcv_xgb_800 = xgb.XGBRegressor()
model_tensile_xgb = xgb.XGBRegressor()

## model declaration (cat)
model_mu_cat_50 = cat.CatBoostRegressor()
model_mu_cat_200 = cat.CatBoostRegressor()
model_mu_cat_400 = cat.CatBoostRegressor()
model_mu_cat_800 = cat.CatBoostRegressor()
model_Pcv_cat_50 = cat.CatBoostRegressor()
model_Pcv_cat_200 = cat.CatBoostRegressor()
model_Pcv_cat_400 = cat.CatBoostRegressor()
model_Pcv_cat_800 = cat.CatBoostRegressor()
model_tensile_cat = cat.CatBoostRegressor()

## model declaration (lgb)
model_mu_lgb_50 = lgb.LGBMRegressor()
model_mu_lgb_200 = lgb.LGBMRegressor()
model_mu_lgb_400 = lgb.LGBMRegressor()
model_mu_lgb_800 = lgb.LGBMRegressor()
model_Pcv_lgb_50 = lgb.LGBMRegressor()
model_Pcv_lgb_200 = lgb.LGBMRegressor()
model_Pcv_lgb_400 = lgb.LGBMRegressor()
model_Pcv_lgb_800 = lgb.LGBMRegressor()
model_tensile_lgb = lgb.LGBMRegressor()



## XGBoost model loading
try:    # model_mu_xgb
    model_mu_xgb_50.load_model(current_path + '/' + folder_xgb + '/' + 'model_mu_xgb_50.json')
except:
    logging.info("Something wrong in loading XGBoost mu_50 model")
try:    # model_mu_xgb
    model_mu_xgb_200.load_model(current_path + '/' + folder_xgb + '/' + 'model_mu_xgb_200.json')
except:
    logging.info("Something wrong in loading XGBoost mu_200 model")
try:    # model_mu_xgb
    model_mu_xgb_400.load_model(current_path + '/' + folder_xgb + '/' + 'model_mu_xgb_400.json')
except:
    logging.info("Something wrong in loading XGBoost mu_400 model")
try:    # model_mu_xgb
    model_mu_xgb_800.load_model(current_path + '/' + folder_xgb + '/' + 'model_mu_xgb_800.json')
except:
    logging.info("Something wrong in loading XGBoost mu_800 model")

###Pcv###
try:    # model_Pcv_xgb
    model_Pcv_xgb_50.load_model(current_path + '/' + folder_xgb + '/' + 'model_Pcv_xgb_50.json')
except:
    logging.info("Something wrong in loading XGBoost Pcv_50 model")
try:    # model_Pcv_xgb
    model_Pcv_xgb_200.load_model(current_path + '/' + folder_xgb + '/' + 'model_Pcv_xgb_200.json')
except:
    logging.info("Something wrong in loading XGBoost Pcv_200 model")
try:    # model_Pcv_xgb
    model_Pcv_xgb_400.load_model(current_path + '/' + folder_xgb + '/' + 'model_Pcv_xgb_400.json')
except:
    logging.info("Something wrong in loading XGBoost Pcv_400 model")
try:    # model_Pcv_xgb
    model_Pcv_xgb_800.load_model(current_path + '/' + folder_xgb + '/' + 'model_Pcv_xgb_800.json')
except:
    logging.info("Something wrong in loading XGBoost Pcv_800 model")
####tensile###
try:    # model_tensile_xgb
    model_tensile_xgb.load_model(current_path + '/' + folder_xgb + '/' + 'model_tensile_xgb.json')
except:
    logging.info("Something wrong in loading XGBoost tensile model")
###################################
## Catboost model load
## mu
try:
    model_mu_cat_50.load_model(current_path + '/' + folder_cat + '/' + 'model_mu_cat_50.json')
except:
    logging.info("Something wrong in loading Catboost mu_50 model")
try:
    model_mu_cat_200.load_model(current_path + '/' + folder_cat + '/' + 'model_mu_cat_200.json')
except:
    logging.info("Something wrong in loading Catboost mu_200 model")
try:
    model_mu_cat_400.load_model(current_path + '/' + folder_cat + '/' + 'model_mu_cat_400.json')
except:
    logging.info("Something wrong in loading Catboost mu_400 model")
try:
    model_mu_cat_800.load_model(current_path + '/' + folder_cat + '/' + 'model_mu_cat_800.json')
except:
    logging.info("Something wrong in loading Catboost mu_800 model")
## Pcv
try:
    model_Pcv_cat_50.load_model(current_path + '/' + folder_cat + '/' + 'model_Pcv_cat_50.json')
except:
    logging.info("Something wrong in loading Catboost mu_50 model")
try:
    model_Pcv_cat_200.load_model(current_path + '/' + folder_cat + '/' + 'model_Pcv_cat_200.json')
except:
    logging.info("Something wrong in loading Catboost mu_200 model")
try:
    model_Pcv_cat_400.load_model(current_path + '/' + folder_cat + '/' + 'model_Pcv_cat_400.json')
except:
    logging.info("Something wrong in loading Catboost mu_400 model")
try:
    model_Pcv_cat_800.load_model(current_path + '/' + folder_cat + '/' + 'model_Pcv_cat_800.json')
except:
    logging.info("Something wrong in loading Catboost mu_800 model")
## Tensile
try:    
    model_tensile_cat.load_model(current_path + '/' + folder_cat + '/' + 'model_tensile_cat.json')
except:
    logging.info("Something wrong in loading XGBoost tensile model")
#########################
## LightGBM model load
## mu
try:
    model_mu_lgb_50 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_mu_lgb_50.pkl')
except:
    logging.info("Something wrong in loading LightGBM mu_50 model")
try:
    model_mu_lgb_200 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_mu_lgb_200.pkl')
except:
    logging.info("Something wrong in loading LightGBM mu_200 model")
try:
    model_mu_lgb_400 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_mu_lgb_400.pkl')
except:
    logging.info("Something wrong in loading LightGBM mu_400 model")
try:
    model_mu_lgb_800 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_mu_lgb_800.pkl')
except:
    logging.info("Something wrong in loading LightGBM mu_800 model")
## Pcv
try:
    model_Pcv_lgb_50 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_Pcv_lgb_50.pkl')
except:
    logging.info("Something wrong in loading LightGBM Pcv_50 model")
try:
    model_Pcv_lgb_200 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_Pcv_lgb_200.pkl')
except:
    logging.info("Something wrong in loading LightGBM Pcv_200 model")
try:
    model_Pcv_lgb_400 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_Pcv_lgb_400.pkl')
except:
    logging.info("Something wrong in loading LightGBM Pcv_400 model")
try:
    model_Pcv_lgb_800 = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_Pcv_lgb_800.pkl')
except:
    logging.info("Something wrong in loading LightGBM Pcv_800 model")
## Tensile
try:    
    model_tensile_lgb = joblib.load(current_path + '/' + folder_lgb + '/' + 'model_tensile_lgb.pkl')
except:
    logging.info("Something wrong in loading LightGBM tensile model")