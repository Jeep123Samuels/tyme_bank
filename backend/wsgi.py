
from app import app


if __name__ == '__main__':
    # Threaded option to enable multiple instances for
    # multiple user access support
    print('dsfd')
    app.run(threaded=True, debug=True, port=5010)
