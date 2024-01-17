from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField(
        "メールアドレス", validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")]
    )
    username = StringField("ユーザー名", validators=[DataRequired()])
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(), EqualTo("pass_confirm", message="パスワードが一致していません")],
    )
    pass_confirm = PasswordField("パスワード(確認)", validators=[DataRequired()])

    grade = IntegerField("学年", validators=[DataRequired()])

    def validate_username(self, field):
        pass

    def validate_email(self, field):
        pass

    def validate_grade(self, field):
        if int(field.data) < 0:
            raise ValidationError("存在しない学年です")
