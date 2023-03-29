MODEL_DICT = {
    "davinci": ["text-davinci-003", -1],
    "curie": ["text-curie-001", -2],
    "babbage": ["text-babbage-001", -3],
    "ada": ["text-ada-001", -4],
    "gpt3.5": ["gpt-3.5-turbo"],
}
MODEL = ["gpt-3.5-turbo", 0]

MY_WRONG = "Background service error, please try again later"
MY_PIC = "0.jpg"
MY_REASON = "talk"

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True  # 设置sqlalchemy自动更跟踪数据库
SQLALCHEMY_ECHO = False  # 查询时会显示原始SQL语句
SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 禁止自动提交数据处理

JSON_AS_ASCII = False

IMG_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AUDIO_EXTENSIONS = {'m4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'wav', 'webm'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
IMG_FOLDER = 'static/img/'
AUDIO_FOLDER = 'static/audio/'
STATIC_FOLDER = 'static/'

QQ_GROUP_URL = 'http://127.0.0.1:5700/send_group_msg'
QQ_PRITE_URL = 'http://127.0.0.1:5700/send_private_msg'
MY_QQ_ID = '1639740481'
