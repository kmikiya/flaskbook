from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


# ユーザ作成クラス
class UserForm(FlaskForm):
    # ユーザフォームのusername属性のラベルとバリデータを設定
    username = StringField(
        "ユーザ名",
        validators=[
            DataRequired(message="ユーザ名は必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ],
    )
