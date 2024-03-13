class Config:
    UPLOAD_FOLDER = 'static/temp'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    SECRET_KEY = "54088" 
    #audio setting
    
class audio_Config:
    audio_model = 2

class Database_Config:
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456', 
        'database': 'emotor'
    }
    get_columns = ['e_newspaper_id','e_newspaper_name','edit_name','abstract','year']
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

