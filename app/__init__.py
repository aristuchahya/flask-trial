from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_restx import Api
from .error_handler import handle_api_exception, handle_http_exception, handle_unexpected_exception, ApiException
from werkzeug.exceptions import HTTPException


db = SQLAlchemy()
ma = Marshmallow()

def app_mvc():
    sentry_sdk.init(
        dsn="https://92ed0acc546b9615fdbd5da6f01a2d5f@o4508379685388288.ingest.de.sentry.io/4508379688796240",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )
    
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)
    
    api = Api(
        app,
        version='1.0',
        title='Products API',
        description='A simple Products API',
        doc='/swagger-ui'
    )
    
    from .routes import product_ns
    api.add_namespace(product_ns, path='/api/v1/products')
    
    app.register_error_handler(ApiException, handle_api_exception)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_unexpected_exception)

    with app.app_context():
        # from .routes import product_bp
        # app.register_blueprint(product_bp)

        db.create_all()
    return app

    
