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


# 新規作成画面
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


# 一覧画面
@crud.route("/users")
def users():
    form = UserForm()
    users = User.query.all()
    # index.htmlに取得したユーザ情報をもっていく
    return render_template("crud/index.html", users=users, form=form)


@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
