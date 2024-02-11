from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# SQLAlchemy をインスタンス化
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLをコンソールログに出力
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f",
    )

    # インスタンス初期化⇒アプリケーションが起動される前にデータベースの接続設定やテーブルの作成などの初期化作業ができる
    db.init_app(app)
    csrf.init_app(app)
    Migrate(app, db)
    # views.pyをインポート
    # crud_views:blueprint名
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app
