import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.content import Content, ClientLogo
from src.routes.user import user_bp
from src.routes.content import content_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(content_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # إضافة بيانات أولية إذا لم تكن موجودة
    if Content.query.count() == 0:
        initial_content = [
            Content(section='header', key='title', value='Portfolio', content_type='text'),
            Content(section='navigation', key='home', value='Home', content_type='text'),
            Content(section='navigation', key='about', value='About', content_type='text'),
            Content(section='navigation', key='projects', value='Projects', content_type='text'),
            Content(section='navigation', key='contact', value="Let's Talk", content_type='text'),
            Content(section='clients', key='title', value='Trusted By +200 Client', content_type='text'),
            Content(section='statistics', key='designs', value='+3000', content_type='text'),
            Content(section='statistics', key='designs_label', value='Design', content_type='text'),
            Content(section='statistics', key='clients', value='+200', content_type='text'),
            Content(section='statistics', key='clients_label', value='Client', content_type='text'),
            Content(section='statistics', key='companies', value='+12', content_type='text'),
            Content(section='statistics', key='companies_label', value='Company', content_type='text'),
            Content(section='statistics', key='experience', value='+7', content_type='text'),
            Content(section='statistics', key='experience_label', value='Years Of Experience', content_type='text'),
        ]
        
        for content in initial_content:
            db.session.add(content)
        
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
