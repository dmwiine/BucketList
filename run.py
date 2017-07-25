import os

from api import create_app

config_name = os.getenv('APP_SETTINGS') 
app = create_app(os.getenv('FLASK_CONFIG') or config_name)

if __name__ == '__main__':
    app.run()
    