from avito import app
from os import environ

if __name__ == '__main__':
    host = environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=int(environ.get('PORT', 8080)))
