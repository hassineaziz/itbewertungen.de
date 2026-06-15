from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf.csrf import CSRFProtect
import yaml

load_dotenv()

db = SQLAlchemy()
migrate = Migrate(db)
csrf = CSRFProtect()
babel = Babel()

def get_locale():
    if request.path.startswith('/en/') or request.path == '/en':
        return 'en'
    return 'de'

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hjshjhdjah_kjshkjdhjs_fallback_secret')
    database_url = os.getenv('SQLALCHEMY_DATABASE_URI', os.getenv('DATABASE_URL', 'sqlite:///blog.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Security Configuration
    is_prod = os.getenv('FLASK_ENV') == 'production' or os.getenv('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    app.config['SESSION_COOKIE_SECURE'] = is_prod
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    if is_prod:
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Proxy Fix for running behind Nginx/reverse proxies
    if is_prod or os.getenv('USE_PROXY_FIX', 'false').lower() == 'true':
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    try:
        with open('config.yaml', 'r') as f:
            site_config = yaml.safe_load(f)
    except Exception:
        site_config = {}
    app.config['SITE_CONFIG'] = site_config
    
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    
    from .sitemap_config import seo_bp
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(views, url_prefix='/en', name='views_en')
    app.register_blueprint(seo_bp, url_prefix='/')
    
    from .models import BlogPost, Category, AffiliateLink
    
    with app.app_context():
        db.create_all()

    class AdminAuthMixin:
        def is_accessible(self):
            return session.get('admin_logged_in') is True
        
        def inaccessible_callback(self, name, **kwargs):
            from flask import redirect, url_for
            return redirect(url_for('views.admin_login'))
    
    class AdminModelView(AdminAuthMixin, ModelView):
        pass
    
    class CustomAdminIndexView(AdminAuthMixin, AdminIndexView):
        pass
    
    admin = Admin(app, name='Blog Admin', index_view=CustomAdminIndexView())
    admin.add_view(AdminModelView(BlogPost, db.session, name='Blog Posts'))

    @app.context_processor
    def inject_site_config():
        from flask import url_for as flask_url_for
        
        def custom_url_for(endpoint, **values):
            force_lang = values.pop('force_lang', None)
            
            # If explicitly forcing a language, handle it
            if force_lang == 'en':
                if endpoint.startswith('views.'):
                    endpoint = endpoint.replace('views.', 'views_en.', 1)
            elif force_lang == 'de':
                if endpoint.startswith('views_en.'):
                    endpoint = endpoint.replace('views_en.', 'views.', 1)
            else:
                # Otherwise, stay in current language automatically
                if request.path.startswith('/en/') or request.path == '/en':
                    if endpoint.startswith('views.'):
                        endpoint = endpoint.replace('views.', 'views_en.', 1)
            
            return flask_url_for(endpoint, **values)

        from .models import BlogPost
        # Get unique categories for navigation
        try:
            categories = db.session.query(BlogPost.category).filter(BlogPost.category.isnot(None)).distinct().all()
            categories = [c[0] for c in categories if c[0]]
        except:
            categories = []
            
        site_config = app.config.get('SITE_CONFIG', {})
        
        return {
            'url_for': custom_url_for,
            'config': site_config,
            'SITE_NAME': site_config.get('brand', {}).get('name', 'Premium Blog'),
            'SITE_DOMAIN': site_config.get('seo', {}).get('domain', 'https://example.com'),
            'SITE_DESCRIPTION': site_config.get('niche', {}).get('home_description', 'Expert insights and reviews.'),
            'TWITTER_HANDLE': site_config.get('seo', {}).get('twitter_handle', '@premium_blog'),
            'PRIMARY_COLOR': site_config.get('brand', {}).get('primary_color', '#2563eb'),
            'nav_categories': categories,
            'admin_logged_in': session.get('admin_logged_in') is True,
            'seo_utils': __import__('website.seo_utils', fromlist=['seo_utils']),
            'current_language': get_locale()
        }
            
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)

    @app.template_filter('markdown')
    def render_markdown(text):
        import markdown
        from markupsafe import Markup
        if not text:
            return ""
        return Markup(markdown.markdown(text))

    return app
