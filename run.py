#!flask/bin/python

# python run.py in dir to start local server

from app import app



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)