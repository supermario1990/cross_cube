import os
from utils import L, get_logger
from server import create_app

print(L("Hello world!"))
app = create_app(os.getenv('KROS_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()
