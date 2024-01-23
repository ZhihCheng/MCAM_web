import speech_recognition as sr
import whisper
from transformers import pipeline
import librosa
class Process_audio:
    def transcribe_whisper(wav_filename,text_line):
        # Whisper 語音識別邏輯
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

        return text_line
        # ...

    def transcribe_google(wav_filename,text_line):
        # Google Speech Recognition 語音識別邏輯
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="zh-TW")
                print("辨識結果:", text)
                text_line['complet'] = 1
                text_line['result'] = text
                return text_line
            except sr.UnknownValueError:
                print("Google Speech Recognition 無法理解音頻")
                text_line['complet'] = 0
                text_line['result'] = '無法理解音頻'
                return text_line
            except sr.RequestError as e:
                print("無法從 Google Speech Recognition 獲得結果; {0}".format(e))
                text_line['complet'] = 0
                text_line['result'] = '無法從 Google Speech Recognition 獲得結果'
                return text_line
            
    def transcribe_whisper_for_pretrained(wav_filename, text_line):
        try:
            pipe = pipeline(model="ZhihCheng/whisper-tiny-zh_motor_first", task="automatic-speech-recognition")
        except Exception as e:
            text_line['complet'] = 0
            text_line['error'] = f"模型加載錯誤: {str(e)}"
            return text_line

        try:
            audio_data, _ = librosa.load(wav_filename, sr=None)
        except Exception as e:
            text_line['complet'] = 0
            text_line['error'] = f"音頻文件加載錯誤: {str(e)}"
            return text_line

        try:
            text = pipe(audio_data)["text"]
        except Exception as e:
            text_line['complet'] = 0
            text_line['error'] = f"語音識別錯誤: {str(e)}"
            return text_line

        text_line['complet'] = 1
        text_line['result'] = text

        return text_line
