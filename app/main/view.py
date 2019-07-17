from datetime import datetime
from flask import current_app, flash, redirect, render_template
from . import main
from .form import BillForm
from app.models import Billing
from app.piastrix import create_sign, send_json
from .. import db
from ..config import currencies, SHOP_ID, PAY_WAY


@main.route('/', methods=('GET', 'POST'))
def index():
    form = BillForm()
    if form.validate_on_submit():
        purchases_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transaction = Billing(amount=form.amount.data,
                              currency=form.currency.data,
                              description=form.description.data,
                              purchases_date=purchases_date)
        db.session.add(transaction)
        db.session.flush()
        shop_order_id = transaction.id
        db.session.commit()
        if form.currency.data == "EUR":
            sign = create_sign(form.amount.data,
                               currencies[form.currency.data],
                               SHOP_ID, shop_order_id)

            url = "https://pay.piastrix.com/ru/pay"
            method = "POST"

            values = {
                "amount": form.amount.data,
                "currency": currencies[form.currency.data],
                "shop_id": SHOP_ID,
                "sign": sign,
                "description": form.description.data,
                "shop_order_id": shop_order_id
            }

            return render_template('form.html', url=url,
                                   method=method, values=values)

        elif form.currency.data == "USD":
            sign = create_sign(form.amount.data,
                               currencies[form.currency.data],
                               SHOP_ID, shop_order_id)
            data = {
                "payer_currency": currencies[form.currency.data],
                "shop_amount": form.amount.data,
                "shop_currency": currencies[form.currency.data],
                "shop_id": SHOP_ID,
                "shop_order_id": shop_order_id,
                "sign": sign,
                "description": form.description.data,
                }

            response = send_json(data)

            if response["error_code"] == 0:
                url = response["data"]["url"]
                return redirect(url)
            else:
                current_app.logger.warning('Error: {}'.format(response))
                flash('Error: {}'.format(response))
                return render_template('index.html', form=form)

        else:
            sign = create_sign(form.amount.data,
                               currencies[form.currency.data], PAY_WAY,
                               SHOP_ID, shop_order_id)
            data = {
                "amount": form.amount.data,
                "currency": currencies[form.currency.data],
                "payway": PAY_WAY,
                "shop_id": SHOP_ID,
                "sign": sign,
                "description": form.description.data,
                "shop_order_id": shop_order_id
            }

            response = send_json(data, invoice=True)

            if response["error_code"] == 0:
                url = response["data"]["url"]
                method = response["data"]["method"]

                values = {
                    "lang": response["data"]["data"]["lang"],
                    "m_curorderid": response["data"]["data"]["m_curorderid"],
                    "m_historyid": response["data"]["data"]["m_historyid"],
                    "m_historytm": response["data"]["data"]["m_historytm"],
                    "referer": response["data"]["data"]["referer"],
                }

                return render_template('form.html', url=url,
                                       method=method, values=values)
            else:
                current_app.logger.warning('Error: {}'.format(response))
                flash('Error: {}'.format(response))
                return render_template('index.html', form=form)

    return render_template('index.html', form=form)
