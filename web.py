# Python標準庫導入pred_output
import cv2 as cv
import os
import numpy as np
import pandas as pd
from functools import wraps
import io
import shutil
import logging
logging.basicConfig(level=logging.INFO)


# 第三方庫導入
from flask import Flask, request, render_template, jsonify, redirect
from werkzeug.utils import secure_filename
import mysql.connector
import soundfile as sf
from pydub import AudioSegment


# 應用程式或局部模組導入
from config import DevelopmentConfig, Config,Database_Config,audio_Config
from determine_str import determine
from Img_Predict.glcm import get_gray_level_feature
from Img_Predict.pred_model_loading import pred_output
from Process_audio import Process_audio
from chinese_number import extract_and_convert_numbers
from find_motor_sentence import find_first_motor

logging.info("Loading parameter model start...")
# 預測模型導入
from sys_py_FeSiCr.parameter_sug_total import FeSiCr_customize,FeSiCr_max_mu_max_tensile,FeSiCr_max_mu_min_pcv
from sys_py_NiFe.parameter_sug_total import Nife_customize,Nife_max_mu_max_tensile,Nife_max_mu_min_pcv

logging.info("Loading parameter model complete")
call_motor_AI = True

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

# import matlab
import matlab.engine
import ollama
from opencc import OpenCC


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def render_page(template):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            return render_template(template)
        return decorated_function
    return decorator



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@render_page('index.html')
def index():
    pass


@app.route('/MPRS', methods=['GET', 'POST'])
@render_page('MPRS.html')
def mprs():
    pass

@app.route('/WCPS', methods=['GET', 'POST'])
@render_page('WCPS.html')
def wcps():
    pass

@app.route('/TSDS', methods=['GET', 'POST'])
@render_page('TSDS.html')
def tsds():
    pass

@app.route('/search', methods=['GET', 'POST'])
@render_page('search.html')
def search():
    pass

@app.route('/Motor', methods=['GET', 'POST'])
@render_page('Motor.html')
def motor():
    pass

@app.route('/motor_coai', methods=['GET', 'POST'])
@render_page('motor_coai.html')
def motor_coai():
    pass

@app.route('/motor_coai2', methods=['GET', 'POST'])
@render_page('motor_coai2.html')
def motor_coai2():
    pass

@app.route('/Two_port', methods=['GET', 'POST'])
@render_page('Two_port.html')
def Two_port():
    pass

@app.route('/MotorMeasurement', methods=['GET', 'POST'])
@render_page('MotorMeasurement.html')
def MotorMeasurement():
    pass

@app.route('/increment', methods=['POST'])
def increment():
    result = {}
    frequency_map = {
        '50': '0',
        '200': '1',
        '400': '2',
        '800': '3',
    }
    data = request.get_json()
    radio_type = data.get('radio_type')
    material = data.get('material')
    frequency = frequency_map.get(data.get('frequency'))
    logging.info(f'Use on {material}')

    def calculate_parameters(func, args):
        out1, out2 = func(args)
        return {
            'p1': float(out2[0]),
            'p2': float(out2[1]),
            'p3': float(out2[2]),
            'p4': float(out2[3]),
            'a1': round(float(out1[0]), 3),
            'a2': round(float(out1[1]), 3),
            'a3': round(float(out1[2]), 3),
        }

    args = [0, frequency]
    if radio_type == 'option3':
        args.extend([data.get('value1'), data.get('value2'), data.get('value3')])

    if material == 'FeSiCr':
        func_map = {
            'option1': FeSiCr_max_mu_min_pcv,
            'option2': FeSiCr_max_mu_max_tensile,
            'option3': FeSiCr_customize,
        }
    else:  # NiFe
        func_map = {
            'option1': Nife_max_mu_min_pcv,
            'option2': Nife_max_mu_max_tensile,
            'option3': Nife_customize,
        }

    func = func_map.get(radio_type)
    if func:
        result = calculate_parameters(func, args)
    else:

        logging.info(f'Invalid radio_type: {radio_type}')
    return jsonify(result)


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
    try:
        data = request.get_json()
        image_path = os.path.join('static', data['imagename'])
        pred_label = data['material']
        pred_frequency = data['frequency']

        img = cv.imread(image_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        feature = get_gray_level_feature(img)
        parm = np.array(data['parm'])
        features = np.array(np.concatenate([feature, parm]))

        pred_list = []
        if pred_label == '0':
            pred_list = ['pmb'+'_'+pred_frequency+'Hz', 'iron'+'_'+pred_frequency+'Hz']
        else:
            pred_list = ['tensile']
        pred_result = {'pred': pred_output(pred_list, features)}

        return jsonify(pred_result)

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
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
    return_dict = {
        'news':0,
        'sentence':'none',
        'two_port_model':'none',
    }
   
    data = request.get_json()
    conn = mysql.connector.connect(**Database_Config.db_config)
    
    cursor = conn.cursor()

    query = "SELECT * FROM e_newspaper_name"
    cursor.execute(query)
    results = cursor.fetchall()

    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(results, columns=columns)
    
    cursor.close()
    conn.close()
    
    result_df = df[df['e_newspaper_name'].str.contains(data['value'], case=False, regex=False)] 
    selected_df = result_df[Database_Config.get_columns]
    return_dict['sentence'] = data['value']
    
    
    sentence = find_first_motor(data['value'])
    logging.info(f'find setence {sentence}')
    return_dict['sentence'] = sentence

    if sentence is not None:
        logging.info('sentence =  ' + sentence)
        result_df = df[df['e_newspaper_name'].str.contains(sentence, case=False, regex=False)] 
        selected_df = result_df[Database_Config.get_columns]

    if len(selected_df) == 0:
        return jsonify(return_dict)
    
    return_dict['news']= selected_df.to_json(orient='records', force_ascii=False)

    try:
        two_port ={
            '永磁直流馬達': 'PMDC_simulink',
            '串激直流馬達': 'SeriesExcited_simulink',
            '它激直流馬達': 'SeparatelyExcited_simulink',
            '並激直流馬達': 'ShuntExcited_simulink',
        }
        
        for key in two_port:
            if key in data['value']:
                return_dict['two_port_model'] = key
                print(key)

        
    except ImportError:
         logging.info("Matlab module is not available.")

    return jsonify(return_dict)

@app.route('/update_chart', methods=['POST'])
def update_chart():
    # 從CSV文件讀取資料
    two_port_model = request.json.get('two_port_model')
    data = pd.read_csv(f'./static/{two_port_model}_output_data.csv')
    data = data[data['efficiency'] > 0]
    # 設定 x 軸資料 (Speed)
    x = data['speed'].tolist()

    # 構建資料字典
    data_dict = {
        "Torque": list(zip(x, data['torque'].tolist())),
        "Efficiency": list(zip(x, data['efficiency'].tolist())),
        "Powerin": list(zip(x, data['powerin'].tolist())),
        "Voltage": list(zip(x, data['voltage'].tolist())),
        "Current": list(zip(x, data['current'].tolist())),
    }

    selected_data = request.json.get('selectedData', [])
    datasets = []

    for data_key in selected_data:
        datasets.append({
            'label': data_key,
            'data': [{'x': x, 'y': y} for x, y in data_dict.get(data_key, [])],
            'borderColor': '',
            'backgroundColor': '',
            'fill': False,
            'showLine': True,
            'yAxisID': ''  # 初始值，前端會動態分配
        })
    
    return jsonify({'datasets': datasets})


@app.route('/run_simulink', methods=['POST'])
def run_simulink():
    return_dict = {
        'L': 0,
        'R': 0,
        'J': 0,
        'B': 0,
        'Ke': 0,
        'Kt': 0,
    }
    data = request.get_json()
    keyword = None
    #find the motor curve
    if '最大功率' in data['value']:
        keyword = '最大功率'#'max_torque'
    if '最高轉速' in data['value']:
        keyword = '最高轉速'#'max_speed'
    try:
        if keyword is not None:
            import matlab
            logging.info('run Matlab')
            ratio = extract_and_convert_numbers(data['value'])
            excel_path = r'./static/parm_table.xlsx'
            df_parm = pd.read_excel(excel_path)
            multiplier_value = df_parm.loc[df_parm[keyword] == ratio, '倍率'].iloc[0] if not df_parm.loc[df_parm[keyword] == ratio, '倍率'].empty else None
            if multiplier_value is not None:
                logging.info("start find curve")
                eng = matlab.engine.start_matlab()
                # 輸入所需參數
                eng.workspace['a']=float(multiplier_value)   
                # 呼叫matlab.M檔
                eng.this_is_for_exhibition(nargout = 0)
                return_dict['L']  = eng.evalin('base', 'L', nargout=1)
                return_dict['R']  = eng.evalin('base', 'R', nargout=1)
                return_dict['J']  = eng.evalin('base', 'J', nargout=1)
                return_dict['B']  = eng.evalin('base', 'B', nargout=1)
                return_dict['Ke'] = eng.evalin('base', 'Ke', nargout=1)
                return_dict['Kt'] = eng.evalin('base', 'Kt', nargout=1)
            else:
                logging.info("no parm found")
    except ImportError:
         logging.info("Matlab module is not available.")
    return jsonify(return_dict)
    

@app.route('/pred_string', methods=['POST'])
def pred_string():
    return_dict = {
        'max_value': 0,
        'type': 0,
        'material': 0,
        'frequency': '50hz',
        'workpice': 0,
        'ration': 0,
    }

    data = request.get_json()
    input_string = data.get('value', '').lower()
    
    return_dict['max_value'], return_dict['type'] = determine.calculate_score(input_string)
    return_dict['frequency'] = determine.determine_frequency(input_string)
    return_dict['material'] = determine.determine_material(input_string)
    return_dict['workpice'] = determine.determine_workpiece(input_string)
    return_dict['ration'] = determine.determine_ratio(input_string)

    return jsonify(return_dict)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    text_line = {'complet': 0, 'result': ""}
    if 'audio_data' in request.files:
        audio_file = request.files['audio_data']
        # 使用 BytesIO 從記憶體讀取音頻數據
        audio_data = io.BytesIO(audio_file.read())
        # 轉換音頻格式
        wav_filename = os.path.join(app.config['UPLOAD_FOLDER'], "audio.wav")

        try:
            if audio_Config.audio_model == 0:
                text_line = Process_audio.transcribe_whisper(wav_filename,text_line)  # 使用 Whisper 進行語音識別
            elif audio_Config.audio_model == 1:
                text_line = Process_audio.transcribe_google(wav_filename,text_line)  # 使用 Google Speech Recognition 進行語音識別
            elif audio_Config.audio_model == 2:
                text_line = Process_audio.transcribe_whisper_for_pretrained(wav_filename,text_line)  # 使用 訓練過的Whisper 進行語音識別
            return jsonify(text_line)
        
        except Exception as e:
            logging.info('no audui file')
            text_line['result'] = str(e)
            return jsonify(text_line)
    else:
        text_line['result'] = '沒有找到音頻檔案'
        return jsonify(text_line)
    
@app.route('/run_alpaca', methods=['POST'])
def run_alpaca():
    print("run_alpaca")
    text_line = {'complet': 0, 
                 'result': "",
                 'curve' : 'False',
                 'twoport' : 'False',
                 'motor' : 'False',
                 'pic' : 'None',
                 }
    
    module_dict = {
        '串激馬達': '串激直流馬達',
        '串激式馬達': '串激直流馬達',
        '串激式有刷馬達': '串激直流馬達',
        '串激式直流有刷馬達': '串激直流馬達',
        '永磁馬達': '永磁直流馬達',
        '永磁式馬達': '永磁直流馬達',
        '永磁式有刷馬達': '永磁直流馬達',
        '永磁式直流有刷馬達': '永磁直流馬達',
        '它激馬達': '它激直流馬達',
        '它激式馬達': '它激直流馬達',
        '它激式有刷馬達': '它激直流馬達',
        '它激式直流有刷馬達': '它激直流馬達',
        '並激馬達': '並激直流馬達',
        '並激式馬達': '並激直流馬達',
        '並激式有刷馬達': '並激直流馬達',
        '並激式直流有刷馬達': '並激直流馬達',
    }

    mission_dice = {'曲線': 'curve', 
                    '架構': 'twoport', 
        }
    
    pic_dict = {
        '電路': 0
    }
    
    
    data = request.get_json()
    
    print(f'data[list] is {data["list"]}')
    if call_motor_AI:
        logging.info("predoct start")
        response = ollama.chat(
            model="lgkt/llama3-chinese-alpaca:latest",
            messages=data["list"]
        )
        cc = OpenCC('s2t') 
        text_line['result'] = cc.convert(response["message"]["content"])

        for keyword in module_dict.keys():
            if keyword in text_line['result']:
                text_line['motor'] = module_dict[keyword]

        for keyword in mission_dice.keys():
            if keyword in data['value']:
                if keyword == '曲線':
                    text_line['curve'] = '''
                                            <form id="data-form">
                                                <label><input type="checkbox" name="data" value="Torque" onchange="updateChart()"> TL(Nm)</label>
                                                <label><input type="checkbox" name="data" value="Efficiency" onchange="updateChart()"> Efficiency(%) </label>
                                                <label><input type="checkbox" name="data" value="Powerin" onchange="updateChart()"> Pin(W)</label>
                                                <label><input type="checkbox" name="data" value="Voltage" onchange="updateChart()"> Voltage(volt)</label>
                                                <label><input type="checkbox" name="data" value="Current" onchange="updateChart()"> Current(A)</label>
                                            </form>
                                            <canvas id="myChart"></canvas>
                                        '''
                if keyword == '架構':
                    text_line['twoport'] = 'False'
        print(text_line)

    else:
        text_line['complet'] = 1
    return jsonify(text_line)

@app.route('/get_two_port_data', methods=['POST'])
def get_two_port_data():
    data = request.json
    print(data)  # 這裡你可以處理收到的數據
    return jsonify({"status": "success", "data": data})
    
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)
    else:
        logging.info(f"資料夾 {folder_path} 不存在，無法清空。") 
        
logging.info("=================Web server is running=================")
if __name__ == '__main__':
    app.secret_key = Config.SECRET_KEY
    # app.debug = False
    app.run('0.0.0.0',port=8152)

    clear_folder(app.config['UPLOAD_FOLDER'])