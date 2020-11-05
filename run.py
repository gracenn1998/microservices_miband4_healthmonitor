# from miband4_pairing import app
# from miband4_database import manager
from user_database import manager

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()