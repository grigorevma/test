from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Length, Required


class BillForm(FlaskForm):
    amount = IntegerField('Сумма оплаты')
    currency = SelectField('Валюта оплаты', choices=[("EUR", "EUR"),
                                                     ("USD", "USD"),
                                                     ("RUB", "RUB")])
    description = StringField('Описание товара',
                              validators=[Required(), Length(1, 64)])
    submit = SubmitField('Оплатить')
