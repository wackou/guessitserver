import os

class GuessitServerConfig(object):
    DEBUG = False
    TESTING = False


class GuessitServerProductionConfig(GuessitServerConfig):
    SERVER_ID = 'production'
    # see: http://flask.pocoo.org/docs/0.10/quickstart/#sessions
    SECRET_KEY = 'not a very good secret key...'
    SQLALCHEMY_DATABASE_URI='sqlite:////var/www/guessitserver/guessit.sqlite3'


class GuessitServerDevelopmentConfig(GuessitServerConfig):
    SERVER_ID = 'development'
    DEBUG = True
    SECRET_KEY = 'not a good secret key either...'
    SQLALCHEMY_DATABASE_URI='sqlite:///guessit.sqlite3'


def get_current_environment_config(config_type = None):
    CONFIG_TYPE = config_type or os.environ.get('GUESSITSERVER_CONFIG', GuessitServerDevelopmentConfig.SERVER_ID)
    settings = None

    if CONFIG_TYPE.lower() == GuessitServerProductionConfig.SERVER_ID:
        settings = GuessitServerProductionConfig
    elif CONFIG_TYPE.lower() == GuessitServerDevelopmentConfig.SERVER_ID:
        settings = GuessitServerDevelopmentConfig

    if not settings:
        raise Exception('"%s" is no a valid configuration for GUESSITSERVER_CONFIG.' % CONFIG_TYPE)

    return settings
