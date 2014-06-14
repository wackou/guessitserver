# -*- coding: utf-8 -*-


from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from guessitserver import frontend
from guessitserver.config import get_current_environment_config, get_current_environment_config_for_api
import logging
log = logging.getLogger(__name__)

settings_override = get_current_environment_config()
settings_override_api = get_current_environment_config_for_api()
log.critical('** Running in %s mode. **'% settings_override.SERVER_ID)

frontend_app = frontend.create_app(settings_override=settings_override)

application = DispatcherMiddleware(frontend_app)


def main():
    print('-'*100)
    print('Registered frontend routes:')
    print(frontend_app.url_map)

    run_simple('0.0.0.0', 5000, application, use_reloader=settings_override.DEBUG,
               use_debugger=settings_override.DEBUG)

if __name__ == "__main__":
    main()
