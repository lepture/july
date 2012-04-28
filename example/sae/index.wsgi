import sae

from app import app
application = sae.create_wsgi_app(app())
