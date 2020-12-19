from miband4_api import app, globals

if __name__ == '__main__':
    globals.init()
    app.run(debug=True, port=5001, host='0.0.0.0')
