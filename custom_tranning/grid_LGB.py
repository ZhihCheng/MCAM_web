import sys
sys.path.append(sys.path[0]+'/../')

from model_dataset.mag_dataset import *
from model_dataset.mach_dataset import *

from sklearn.metrics import r2_score

import lightgbm as lgb
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_squared_error

import json



# Tuning parameter

# n_estimators: tree number
# max_depth: the maximum depth for each tree
# learning_rate
# colsample_bytree: a family of parameters for subsampling of columns


n_estimators = [int(x) for x in np.linspace(start=10, stop=500, num=11)]  # default = 100
max_depth = [int(x) for x in np.linspace(2, 8, num=4)] # default = 6
learning_rate = [round(float(x), 2) for x in np.linspace(start= 0.01, stop= 0.3, num=10)]   # default = 0.03
colsample_by_tree = [round(float(x), 2) for x in np.linspace(start=0.1, stop=1, num=10)]    # default = 1

params = {'n_estimators': n_estimators,
          'max_depth': max_depth,
          'learning_rate': learning_rate,
        #   'colsample_bytree': colsample_by_tree
          }
# params['tree_method'] = ['gpu_hist']

# print(params)

lgb_mu_50 = lgb_mu_200 = lgb_mu_400 = lgb_mu_800 = lgb.LGBMRegressor(objective='regression',
                            num_leaves=31,
                            learning_rate=0.1,
                            n_estimators=100)
lgb_Pcv_50 = lgb_Pcv_200 = lgb_Pcv_400 = lgb_Pcv_800 = lgb.LGBMRegressor(objective='regression',
                            num_leaves=31,
                            learning_rate=0.1,
                            n_estimators=100)


lgb_yield = lgb.LGBMRegressor(objective='regression',
                            num_leaves=31,
                            learning_rate=0.1,
                            n_estimators=100)
lgb_tensile = lgb.LGBMRegressor(objective='regression',
                            num_leaves=31,
                            learning_rate=0.1,
                            n_estimators=100)

def grid(model_name, model_list, data_list, label_list):
    output = {}
    for (name, model, data, label) in zip(model_name, model_list, data_list, label_list):
        print(f"{name}\n")
        reg = RandomizedSearchCV(model,
                        params,
                        scoring='r2',
                        n_iter=100
                        ,verbose=1)
        reg.fit(data, label.ravel())
        output[name] =  reg.best_params_
        # print("Best parameters:", reg.best_params_)
        print(output[name])
    return output 
        

if __name__ == "__main__":
    mu_name_list = ['50Hz', '200Hz', '400Hz', '800Hz']
    mu_grid_model_list = [lgb_mu_50, lgb_mu_200, lgb_mu_400, lgb_mu_800]
    mu_data_list = [train_mu_data_50, train_mu_data_200, train_mu_data_400, train_mu_data_800]
    mu_label_list = [train_mu_label_50, train_mu_label_200, train_mu_label_400, train_mu_label_800]
    mu_grid_param = grid(mu_name_list, mu_grid_model_list, mu_data_list, mu_label_list)
    
    Pcv_name_list = ['50Hz', '200Hz', '400Hz', '800Hz']
    Pcv_grid_model_list = [lgb_Pcv_50, lgb_Pcv_200, lgb_Pcv_400, lgb_Pcv_800]
    Pcv_data_list = [train_Pcv_data_50, train_Pcv_data_200, train_Pcv_data_400, train_Pcv_data_800]
    Pcv_label_list = [train_Pcv_label_50, train_Pcv_label_200, train_Pcv_label_400, train_Pcv_label_800]
    Pcv_grid_param = grid(Pcv_name_list, Pcv_grid_model_list, Pcv_data_list, Pcv_label_list)

    yield_name_list =['yield']
    yield_grid_model_list = [lgb_yield]
    yield_data_list = [train_yield_data]
    yield_label_list = [train_yield_label]
    yield_grid_param = grid(yield_name_list, yield_grid_model_list, yield_data_list, yield_label_list)

    tensile_name_list = ['tensile']
    tensile_grid_model_list = [lgb_tensile]
    tensile_data_list = [train_yield_data]
    tensile_label_list = [train_tensile_label]
    tensile_grid_param = grid(tensile_name_list, tensile_grid_model_list, tensile_data_list, tensile_label_list)



    lgb_grid_param = {'mu': mu_grid_param,
            'Pcv': Pcv_grid_param,
            'yield': yield_grid_param,
            'tensile': tensile_grid_param}

    with open('grid_param_output\\lgb_grid_param.txt', 'w') as f:
        json.dump(lgb_grid_param,f)

    # print("Best parageters:", reg.best_params_)


