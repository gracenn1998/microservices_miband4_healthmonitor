from miband4_flask import app
from database import manager

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()