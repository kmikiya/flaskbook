from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from apps.config import config
import os

# SQLAlchemy をインスタンス化
db = SQLAlchemy()
csrf = CSRFProtect()
config_key = os.getenv("FLASK_APP_CONFIG_KEY")


# config_keyは環境変数から取得
def create_app():
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    # インスタンス初期化⇒アプリケーションが起動される前にデータベースの接続設定やテーブルの作成などの初期化作業ができる
    db.init_app(app)
    csrf.init_app(app)
    Migrate(app, db)
    # views.pyをインポート
    # crud_views:blueprint名
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # 認証機能
    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    return app
