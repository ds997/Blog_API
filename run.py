# import os
#
# from src.app import create_app
#
# if __name__ == '__main__':
#     env_name = os.getenv('FLASK_ENV')
#     app = create_app(env_name)
#     port = os.getenv('PORT')
#     # run app
#     app.run(host='0.0.0.0', port=port)
#
#     # run app
#     app.run()

import os

from src.app import create_app

if __name__ == '__main__':
    env_name = os.getenv('FLASK_ENV')
    app = create_app(env_name)
    # run app
    app.run()
