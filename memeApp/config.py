class Config(object):
	SECRET_KEY = 'asdjf93fjkandkfna;3knfa;klsnef;i8nKNf;k3nK3kn'
	
class DevConfig(Config):
	DEBUG = True
	UPLOAD_FOLDER = '/app/static/images'


config = {
	'default': DevConfig,
	'development': DevConfig
}
