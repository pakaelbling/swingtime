import os
class Config:
    #Obviously, the secret key would be handled better for real applications
    SECRET_KEY = 'b9216efa4d97a0399eef0cee6f8ca1c3de8575fcde011c7aae6415d332860388'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #Hid the email account information in environment variables, used to send password reset tokens
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
