# from Img_Predict.glcm import get_gray_level_feature
# import cv2 as cv
# import os
# from tqdm import tqdm
# import pandas as pd
# fold_path = './static/circle(340x344)/'
# for  i in tqdm(os.listdir(fold_path)):
#     feature_list = []
#     for j in range(1,201):
#         if j < 10:
#             count = '0'+str(j)
#         else:
#             count = j
#         file_path = os.path.join(fold_path, i,'layer_'+str(count)+'.jpg')
#         img = cv.imread(file_path)
#         img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#         feature = get_gray_level_feature(img)
#         feature_list.append(feature)
#     df = pd.DataFrame(feature_list)
#     df.to_excel(os.path.join(fold_path,i,'GLCM_feature.xlsx'), index=False)

from Img_Predict.glcm import get_gray_level_feature
import cv2 as cv
import os
from tqdm import tqdm
import pandas as pd
# fold_path = './static/circle(340x344)/'
fold_path = './static/sectionview/'
for  i in tqdm(os.listdir(fold_path)):
    feature_list = []
    for j in range(0,359):
        # if j < 10:
        #     count = '0'+str(j)
        # else:
        #     count = j
        # file_path = os.path.join(fold_path, i,'layer_'+str(count)+'.jpg')
        file_path = os.path.join(fold_path, i,'angle_'+str(j)+'_RGB.png')
        img = cv.imread(file_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        feature = get_gray_level_feature(img)
        feature_list.append(feature)
    df = pd.DataFrame(feature_list)
    df.to_excel(os.path.join(fold_path,i,'GLCM_feature.xlsx'), index=False)