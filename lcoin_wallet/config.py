import os 

class Config():
    if os.path.exists(os.getcwd() + '/lcoin_wallet/config.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read(os.getcwd() + '/lcoin_wallet/config.ini')
        SECRET_KEY = config['SERVER']['SECRET_KEY']
        SQLALCHEMY_DATABASE_URI = config['SERVER']['DATABASE_URI']
        SQLALCHEMY_TRACK_MODIFICATIONS = False

        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = config['EMAIL']['EMAIL_USER']
        MAIL_PASSWORD = config['EMAIL']['EMAIL_PASS']
    else:
        SECRET_KEY = os.environ.get("SECRET_KEY")
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres", "postgresql")
        SQLALCHEMY_TRACK_MODIFICATIONS = False

        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = os.environ.get('EMAIL_USER')
        MAIL_PASSWORD = os.environ.get('EMAIL_PASS')