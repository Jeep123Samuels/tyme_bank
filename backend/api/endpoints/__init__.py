from .accounts import accounts_bp
from .health import health_bp
from .transactions import transactions_bp

GLOBAL_BLUEPRINTS: list = [
    accounts_bp,
    health_bp,
    transactions_bp,
]
