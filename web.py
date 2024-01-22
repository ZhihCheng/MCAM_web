from flask import Flask, request, render_template, jsonify
from flask import redirect, url_for
from werkzeug.utils import secure_filename
from sys_py_FeSiCr.parameter_sug_max_mu_min_pcv import *
from sys_py_FeSiCr.parameter_sug_max_mu_max_tensile import *
from sys_py_FeSiCr.parameter_sug_customize import *
from sys_py_NiFe.parameter_sug_max_mu_min_pcv import *
from sys_py_NiFe.parameter_sug_max_mu_max_tensile import *
from sys_py_NiFe.parameter_sug_customize import *
from Img_Predict.pred_model_loading import pred_output
from Img_Predict.glcm import get_gray_level_feature
import cv2 as cv
import pandas as pd
import speech_recognition as sr
import whisper
import mysql.connector
from pydub import AudioSegment
recognizer = sr.Recognizer()
app = Flask(__name__)


MPRS_keyword = {
    '參數建議系統':100,
    '材料':8,
    'FeSiCr':8,
    'NiFe':8,
    '高磁導率':8,
    '低鐵損':8,
    '高最大拉伸':8,
    '高拉伸強度':8,
    '客製化':8,
    '參數':8,
    '最佳化':8,
    '建議':8,
}

TSDS_keyword = {
    '生產履歷':100,
    '剖面':100,
    '縱切面':100,
}

WCPS_keyword = {
    '工件特性預測':100,
    '預測':8,
    '預估':8,
    '逐層圖像':8,
    '磁特性':8,
    '圓環':8,
    '狗骨頭':8,
    '積層圖像':8,
    '積層影像':8,
    '積層製造圖像':8,
    '積層製造影像':8,
}


UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
get_columns = ['e_newspaper_id','e_newspaper_name','edit_name','abstract','year']
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'emotor'
}

audio_model = 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/MPRS', methods=['GET', 'POST'])
def MPRS():
    return render_template('MPRS.html')


@app.route('/WCPS', methods=['GET', 'POST'])
def WCPS():
    return render_template('WCPS.html')

@app.route('/TSDS', methods=['GET', 'POST'])
def TSDS():
    return render_template('TSDS.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route('/Motor', methods=['GET', 'POST'])
def Motor():
    return render_template('Motor.html')

@app.route('/paper', methods=['GET', 'POST'])
def paper():
    return render_template('paper.html')

@app.route('/increment', methods=['POST'])
def increment():
    dict = {}
    frequency = {
        '50':'0',
        '200':'1',
        '400':'2',
        '800':'3',
    }
    data = request.get_json()
    raiod_type = data['radio_type']
    print(data)
    raiod_type = data['radio_type']
    if data['material'] == 'FeSiCr':
        print(f'Use on FeSiCr')
        if raiod_type =='option1':
            out1,out2 = FeSiCr_max_mu_min_pcv([0,frequency[data['frequency']]])
        elif raiod_type == 'option2':
            out1,out2 = FeSiCr_max_mu_max_tensile([0,frequency[data['frequency']]])
        elif raiod_type == 'option3':
            out1,out2 = FeSiCr_customize([0,frequency[data['frequency']],data['value1'],data['value2'],data['value3']])
    else:
        print(f'Use on NiFe')
        if raiod_type =='option1':
            out1,out2 = Nife_max_mu_min_pcv([0,frequency[data['frequency']]])
        elif raiod_type == 'option2':
            out1,out2 = Nife_max_mu_max_tensile([0,frequency[data['frequency']]])
        elif raiod_type == 'option3':
            out1,out2 = Nife_customize([0,frequency[data['frequency']],data['value1'],data['value2'],data['value3']])
    
    dict['p1'] = float(out2[0])
    dict['p2'] = float(out2[1])
    dict['p3'] = float(out2[2])
    dict['p4'] = float(out2[3])

    dict['a1'] = round(float(out1[0]),3)
    dict['a2'] = round(float(out1[1]),3)
    dict['a3'] = round(float(out1[2]),3)
    return jsonify(dict)




@app.route('/get_glcm_list', methods=['POST'])
def get_glcm_list():
    pred_result = {}
    data = request.get_json()
    init_path = data['init_feature']
    horz_path = data['horz_feature']

    init_path = os.path.join(init_path,'GLCM_feature.xlsx')
    horz_path = os.path.join(horz_path,'GLCM_feature.xlsx')
    init = pd.read_excel(init_path)
    horz = pd.read_excel(horz_path)
    pred_result['init_feature'] = init.to_numpy().tolist()
    pred_result['horz_feature'] = horz.to_numpy().tolist()
    return jsonify(pred_result)

@app.route('/predict', methods=['POST'])
def predict():
    pred_result = {}
    data = request.get_json()
    print(data['imagename'])
    image_path = os.path.join('static',data['imagename'])
    pred_label = data['material']
    pred_frequency = data['frequency'] 
    
    img = cv.imread(image_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    feature = get_gray_level_feature(img)
    parm =np.array(data['parm'])
    features = np.array(np.concatenate([feature, parm]))

    # pred_label
    if pred_label == '0':
        print('pred pmb & iron')
        pred_list = ['pmb'+'_'+pred_frequency+'Hz','iron'+'_'+pred_frequency+'Hz']
        pred_result['pred'] = pred_output(pred_list,features)
    else:
        print('pred tenselie')
        pred_list = ['tensile']
        pred_result['pred'] = pred_output(pred_list,features)
    
    print(pred_result)

    return jsonify(pred_result)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    print(type(file))
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        return jsonify({'result': 'success', 'image_url': file_path})
    return jsonify({'result': 'failure'})


@app.route('/search_database', methods=['POST'])
def search_database():
    data = request.get_json()
    print(data)
    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()

    query = "SELECT * FROM e_newspaper_name"
    cursor.execute(query)
    results = cursor.fetchall()

    columns = [i[0] for i in cursor.description]
    # print(columns)
    df = pd.DataFrame(results, columns=columns)
    
    cursor.close()
    conn.close()
    # if data['type'] == '1':
    #     result_df = df[df['edit_name'].str.contains(data['value'], case=False, regex=False)] 
    # elif data['type'] == '2':
    result_df = df[df['e_newspaper_name'].str.contains(data['value'], case=False, regex=False)] 
    selected_df = result_df[get_columns]
    # print(type(selected_df))
    if len(selected_df) == 0:
        selected_df = 0
        print("hi")
        return jsonify(selected_df)
    
    return jsonify(selected_df.to_json(orient='records', force_ascii=False))

@app.route('/pred_string', methods=['POST'])
def pred_string():
    return_dict ={
        'max_value':0,
        'type':0,
        'material':0,
        'frequency':'50hz',
        'workpice':0,
        'ration':0,
    }
    data = request.get_json()
    input_string = data['value'].lower()
    print(input_string)
    keyword_list = [MPRS_keyword,WCPS_keyword,TSDS_keyword]
    result = []
    for keyword in keyword_list:
        score = 0
        for keyword, value in keyword.items():
            if keyword in input_string:
                score += value
        result.append(score)

    #set_return_dict
    return_dict['max_value'] = max(result)
    return_dict['type'] = result.index(max(result))

    if '50hz' in input_string:
        return_dict['frequency'] = '50hz'
    elif '200hz' in input_string:
        return_dict['frequency'] = '200hz'
    elif '400hz' in input_string:
        return_dict['frequency'] = '400hz'
    elif '800hz' in input_string: 
        return_dict['frequency'] = '800hz'
    
    if 'FeSiCr' in input_string:
        return_dict['material'] = 0
    elif 'NeFi' in input_string:
        return_dict['material'] = 1

    if '圓環' in input_string:
        return_dict['workpice'] = 0
    elif '狗骨頭' in input_string:
        return_dict['workpice'] = 1
    
    if '低鐵損' in input_string:
        return_dict['ration']=0
    elif '高最大拉伸' in input_string:
        return_dict['ration']=1
    elif '高拉伸強度' in input_string:
        return_dict['ration']=1
    elif '客製化' in input_string:
        return_dict['ration']=2
    print(return_dict)
    return jsonify(return_dict)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    text_line = {
        'complet': 0,
        'result' : ""
    }
    if 'audio_data' in request.files:
        temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], "temp_audio")
        # audio_file.save(temp_filename)  # 儲存原始音頻檔案

        # 轉換音頻格式
        wav_filename = os.path.join(app.config['UPLOAD_FOLDER'], "audio.wav")
        # sound.export(wav_filename, format="wav")  # 轉換原始音頻並儲存為 WAV 格式
        # print(wav_filename)


        if audio_model == 0 :
            # 使用 Whisper 進行語音識別
            model = whisper.load_model("base")  # 或選擇其他適合的模型大小
            result = model.transcribe(wav_filename, language="Mandarin")
            text = result["text"]
            print("辨識結果:", text)

            if text:
                text_line['complet'] = 1
                text_line['result'] = text
            else:
                text_line['complet'] = 0
                text_line['result'] = '無法理解音頻'

            return jsonify(text_line)
        
        elif audio_model == 1 :
            # 使用 speech_recognition 進行語音識別
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_filename) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="zh-TW")
                    print("辨識結果:", text)
                    text_line['complet'] = 1
                    text_line['result'] = 'text'
                    return jsonify(text_line)
                except sr.UnknownValueError:
                    print("Google Speech Recognition 無法理解音頻")
                    text_line['complet'] = 0
                    text_line['result'] = '無法理解音頻'
                    return jsonify(text_line)
                except sr.RequestError as e:
                    print("無法從 Google Speech Recognition 獲得結果; {0}".format(e))
                    text_line['complet'] = 0
                    text_line['result'] = '無法從 Google Speech Recognition 獲得結果'
                    return jsonify(text_line)

            
            
if __name__ == '__main__':
    app.debug = True
    app.secret_key = "54088"
    app.run('0.0.0.0',port=8152,ssl_context=('server.crt', 'server.key'))