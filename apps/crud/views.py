from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for

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


@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)
