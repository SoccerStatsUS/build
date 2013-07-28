from main import create_app
from main import ProductionConfig

__all__ = ['application']

application = create_app(ProductionConfig())
