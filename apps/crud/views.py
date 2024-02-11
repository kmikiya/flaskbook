from apps.app import db
from apps.crud.models import User
from flask import Blueprint, render_template

# "crud":blueprint アプリ名
# __name__：アプリのパッケージ名
# "templates":crud/templates内のファイルが参照可能
# "static":crud/static内のファイルが参照可能
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
def sql():
    db.session.query(User).filter_by(id=1).delete()
    db.session.commit()
    db.session.query(User).filter_by(id=1, username="admin").all()
    return "コンソールログを確認して下さい"
