def find_first_motor(sentence):
    # 讀取馬達列表
    with open("./static/motor_list.txt", 'r', encoding='utf-8') as file:
         motors = [line.replace(" ", "") for line in file.readlines()]
    # 移除換行符並進行比對
    for motor in motors:
        motor = motor.strip()  # 移除換行符和頭尾的空格
        if motor:  # 確保motor不是空字串
            if motor in sentence:
                print(f"找到馬達: {motor}")
                print(f"片句: {sentence}")
                return motor
    return None
