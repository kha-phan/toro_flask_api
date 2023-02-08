from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from flask import Flask

from api_configurations import EmployeeApi, StoreApi
from utils.definition import version_prefix
from utils import custom_api, config


app = Flask('flask')
app.executor = ThreadPoolExecutor(max_workers=5)

if not app.debug:
    app.config['RESTFUL_JSON'] = {
        'separators': (',', ':')
    }

api = custom_api.CustomApi(app)


@app.route('/')
def home():
    return "Welcome to Toro app"


@app.route('/health/live')
def live_check():
    return 'ok', 200


@app.route('/health/ready')
def ready_check():
    from module.redis.redis_client import check_redis
    from module.databases.database import Database
    services = {
        'redis': check_redis,
        'db': Database().check
    }
    with ThreadPoolExecutor() as executor:
        services = {k: executor.submit(v) for k, v in services.items()}
        executor.shutdown(wait=True)
        services = {k: v.result() for k, v in services.items()}
    ready = all(v[0] for v in services.values())
    return {
               'status': 'ok' if ready else 'failed',
               'timestamp': datetime.utcnow().timestamp(),
               'services': {
                   name: {
                       'ready': status[0],
                       'time': status[1],
                   } for name, status in services.items()
               }
           }, 200 if ready else 500


api.add_resource(EmployeeApi, f'{version_prefix}/employee')
api.add_resource(StoreApi, f'{version_prefix}/store')

# if config.get('license_service.fetch_at_startup'):
#     from utils.tasks import prepare_to_fetch_licenses
#
#     app.executor.submit(prepare_to_fetch_licenses)
