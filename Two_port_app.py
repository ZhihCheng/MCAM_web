
import matlab.engine
from PIL import Image



def two_port_model(data):
# 輸入所需參數
    eng = matlab.engine.start_matlab()

    eng.workspace['dataStruct'] = matlab.struct(data)
    # eng.workspace['cmd'] = data['cmd']
    # eng.workspace['StopTime'] = data['StopTime']  

    # eng.workspace['Vdc'] = data[']Vdc']
    # eng.workspace['R0'] = data['R0']
    # eng.workspace['Vp'] = data['Vp']

    # eng.workspace['L'] = data['L']
    # eng.workspace['R'] = data['R']
    # eng.workspace['Ke'] = data['Ke']
    # eng.workspace['J'] =  data['J']
    # eng.workspace['Bm'] = data['Bm']
    # eng.workspace['Kt'] = data['Kt']
    # eng.workspace['Ks'] = data['Ks']
    # eng.workspace['Ji'] = data['Ji']
    # eng.workspace['Bi'] = data['Bi']
    # eng.workspace['Ri'] = data['Ri']
    # eng.workspace['Jo'] = data['Jo']
    # eng.workspace['Bo'] = data['Bo']
    # eng.workspace['Ro'] = data['Ro']
    # eng.workspace['KJB'] = 15000 
    # eng.workspace['BL'] = 0

    # eng.workspace['f_v'] = 300 
    # eng.workspace['zeta_v'] = 0.8660 
    # eng.workspace['Kp_w'] = 0
    # eng.workspace['Ki_w'] = 0
    # eng.workspace['Kd_w'] = 0

    # eng.workspace['f_i'] = 1500
    # eng.workspace['zeta_i'] = 0.8660
    # eng.workspace['Kp_i'] = 0
    # eng.workspace['Ki_i'] = 0
    # eng.workspace['Current'] = 'PI'
    # eng.workspace['Velocity'] = 'IP'



    eng.workspace['wcw_i'] = 0



    eng.workspace['wn_v'] = 0
    eng.workspace['K_A'] = 1
    eng.workspace['K1_B'] = 1
    eng.workspace['K2_B'] = 1
    eng.workspace['K_C'] = 1

    #ismodelinerror

    eng.workspace['L_r'] = 0.0380
    eng.workspace['R_r'] = 7.5500
    eng.workspace['Ke_r'] = 0.2100
    eng.workspace['J_r'] = 5.7000e-04
    eng.workspace['Bm_r'] = 5.5000e-05
    eng.workspace['Kt_r'] = 0.2100

    #isdisturbance

    eng.workspace['dis'] = 0.0
    eng.workspace['f_t'] = 0.0
    eng.workspace['t_t'] = 0.0






    

    eng.controller(nargout=0)
    # eng.quit()

    image = Image.open('controller_class.png')
    cropped_image = image.crop((1280, 460, 2786, 870))
    cropped_image.save('controller_class.png')