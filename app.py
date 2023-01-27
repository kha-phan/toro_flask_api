from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from flask import Flask

from resources import ConfigResource, OperatorResource, LicenseResource, ResponseResource, BoundaryResource, \
                      AffiliateLinkResource, FaqResource
from definitions import version_prefix
from utils import custom_api, config


app = Flask('flask')
app.executor = ThreadPoolExecutor(max_workers=5)

# use these separators for minimal response size
if not app.debug:
    app.config['RESTFUL_JSON'] = {
        'separators': (',', ':')
    }

api = custom_api.CustomApi(app)


@app.route('/')
def home():
    return "Welcome to BetFinder API"


@app.route('/health/live')
def live_check():
    return 'ok', 200


@app.route('/health/ready')
def ready_check():
    from utils.redis_client import check_redis
    from databases.database import Database
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

api.add_resource(BoundaryResource, f'{version_prefix}/boundaries')
api.add_resource(LicenseResource, f'{version_prefix}/license')
api.add_resource(ResponseResource, f'{version_prefix}/response')

if config.get('license_service.fetch_at_startup'):
    from utils.tasks import prepare_to_fetch_licenses

    app.executor.submit(prepare_to_fetch_licenses)
