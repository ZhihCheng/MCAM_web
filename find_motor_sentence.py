def find_first_motor(sentence):
    # 讀取馬達列表
    with open("./static/motor_list.txt", 'r', encoding='utf-8') as file:
        motors = file.readlines()
    
    # 移除換行符並進行比對
    for motor in motors:
        motor = motor.strip()  # 移除換行符
        if motor in sentence:
            return motor
    return None
