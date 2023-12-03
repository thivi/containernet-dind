import sys
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    with open("log.txt", "r+", encoding='utf8') as log:
        log.seek(0)
        content = log.read()
        ind = int(content) if content else 0
        log.seek(0)
        log.write(str(ind + 1))

    return f'Hello World from {sys.argv[1]}: index {ind}!\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
