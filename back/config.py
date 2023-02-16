from private import DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE

MODEL_LIST = [
    "text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"
]

MY_WRONG = "Background service error, please try again later"
MY_PIC = "0.jpg"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True  # 设置sqlalchemy自动更跟踪数据库
SQLALCHEMY_ECHO = True  # 查询时会显示原始SQL语句
SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 禁止自动提交数据处理
JSON_AS_ASCII = False
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOAD_FOLDER = 'img/'
