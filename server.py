from flask import Flask
app = Flask(__name__)

from app import views

@app.route("/")
def root():
    return app.send_static_file('/static/pages/index.html')
    
@app.route("/hello")
def hello():
    print(url_for('static', filename='bob.html'))
    return "HI"

if __name__ == "__main__":
    app.run()
