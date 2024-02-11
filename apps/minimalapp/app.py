# from flask import Flask, render_template, url_for, current_app, g
from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    make_response,
    session,
)
from flask_debugtoolbar import DebugToolbarExtension
import logging
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)

# メールクラスのコンフィグ
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)


@app.route("/")
def index():
    return "Hello, FlaskBook!"


@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello {name}"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))
    response.set_cookie("flaskbook key", "flaskbook value")
    session["username"] = "ichiro"
    return response
    # return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    app.logger.debug("debug")
    if request.method == "POST":
        # form属性を使ってフォームの値を取得
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True
        if not username:
            flash("ユーザ名は必須です")

        if not email:
            flash("メールアドレスは必須です")

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")

        if not is_valid:
            return redirect(url_for("contact"))

        # メール送信
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        flash(
            "問い合わせ内容はメールにて送信しました。問い合わせありがとうございました。"
        )
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")


# メール送信関数
# to:送り先
# subject:表題
# template:メールのテンプレート
# **kwargs:
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


with app.test_request_context():
    # /
    print(url_for("index"))
    # hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/ichiro?page=1
    print(url_for("show_name", name="ichiro", page="1"))
    print(url_for("static", filename="style.css"))

with app.test_request_context("/users?updated=true"):
    # trueが入力される
    print(request.args.get("updated"))

""" print(current_app)

ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection = "connection"
print(g.connection)
 """
