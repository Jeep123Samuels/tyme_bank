from flask import make_response
from flask_openapi3 import APIBlueprint

health_bp = APIBlueprint(
    'health',
    __name__,
)


@health_bp.get('/health')
def health():
    return make_response({'status': 'GREEN'}, 200)
