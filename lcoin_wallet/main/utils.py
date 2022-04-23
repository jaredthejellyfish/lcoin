from lcoin_wallet.models import Request, Transaction
from lcoin_wallet.models import Transaction, Request
import requests
import datetime


def check_if_pending(current_user):
    by_user = Request.query.filter_by(by=current_user.username, active=True)
    to_user = Request.query.filter_by(to=current_user.username, active=True)

    return [by_user.first() is not None, to_user.first() is not None], [by_user, to_user]


def get_transactions(current_user):
    sent = []
    received = []

    sent_ = Transaction.query.filter_by(by=current_user.username)
    received_ = Transaction.query.filter_by(to=current_user.username)

    for transaction in sent_:
        sent.append(["Sent", transaction.date,
                    transaction.to, transaction.amount, transaction.concept])

    for transaction in received_:
        received.append(["Received", transaction.date,
                        transaction.by, transaction.amount, transaction.concept])

    lists = sorted(sent + received, key=lambda x: x[1])

    return lists[::-1]


def get_btc_price():
    response = requests.get(
        'https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return (1 / float(data["bpi"]["EUR"]["rate"].replace(',', ''))) * 10


def transaction_html_constructor(transactions, btc_price):
    transactions_html = ''
    transactions = transactions[:5]

    for i in range(len(transactions)):
            if i == 0:
                if transactions[i][4] is '':
                    fromatted_base = f"""
                    <span  tabindex="0" class="" role="button" data-toggle="popover" data-trigger="focus" data-placement="top" data-content="{transactions[i][1].strftime('%d-%m-%Y')}">
                        <div name="transaction" class="flex-container" style="margin-top: -20px; padding-left: 4%;">
                            <div class="flex-child">
                                <p class="bold_text" style="margin-left: 0;">{transactions[i][0]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-left: 0; font-size: 80%;">{transactions[i][2]}</p>
                            </div>
                            <div class="flex-child" style="text-align: right; margin-bottom: 20px;">
                                <p class="bold_text" style="margin-right: 10%;">{'-' if transactions[i][0] == 'Sent' else '+'} ₺{transactions[i][3]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-right: 10%; font-size: 80%;">{'-' if transactions[i][0] == 'Sent' else '+'} {round((btc_price * float(transactions[i][3])), 6)} BTC</p>
                            </div>
                        </div>
                    </span>
                    <hr class="dashed">
                    """.replace('\n', '')

                else:
                    fromatted_base = f"""
                    <span  tabindex="0" class="" role="button" data-toggle="popover" data-trigger="focus" data-placement="top" title="{transactions[i][1].strftime('%d-%m-%Y')}" data-content="{transactions[i][4].capitalize()}">
                        <div name="transaction" class="flex-container" style="margin-top: -20px; padding-left: 4%;">
                            <div class="flex-child">
                                <p class="bold_text" style="margin-left: 0;">{transactions[i][0]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-left: 0; font-size: 80%;">{transactions[i][2]}</p>
                            </div>
                            <div class="flex-child" style="text-align: right; margin-bottom: 20px;">
                                <p class="bold_text" style="margin-right: 10%;">{'-' if transactions[i][0] == 'Sent' else '+'} ₺{transactions[i][3]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-right: 10%; font-size: 80%;">{'-' if transactions[i][0] == 'Sent' else '+'} {round((btc_price * float(transactions[i][3])), 6)} BTC</p>
                            </div>

                        </div>
                    </span>
                    <hr class="dashed">
                    """.replace('\n', '')

            elif i == len(transactions) - 1:
                if transactions[i][4] is '':
                    fromatted_base = f"""
                    <span  tabindex="0" class="" role="button" data-toggle="popover" data-trigger="focus" data-placement="top" data-content="{transactions[i][1].strftime('%d-%m-%Y')}">
                        <div name="transaction" class="flex-container" style="margin-top: -20px; padding-left: 4%; margin-bottom: 10px;">
                            <div class="flex-child">
                                <p class="bold_text" style="margin-left: 0;">{transactions[i][0]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-left: 0; font-size: 80%;">{transactions[i][2]}</p>
                            </div>
                            <div class="flex-child" style="text-align: right; margin-bottom: 20px;">
                                <p class="bold_text" style="margin-right: 10%;">{'-' if transactions[i][0] == 'Sent' else '+'} ₺{transactions[i][3]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-right: 10%; font-size: 80%;">{'-' if transactions[i][0] == 'Sent' else '+'} {round((btc_price * float(transactions[i][3])), 6)} BTC</p>
                            </div>
                        </div>
                    </span>
                    """.replace('\n', '')
                else:
                    fromatted_base = f"""
                    <span  tabindex="0" class="" role="button" data-toggle="popover" data-trigger="focus" data-placement="top" title="{transactions[i][1].strftime('%d-%m-%Y')}" data-content="{transactions[i][4].capitalize()}">
                        <div name="transaction" class="flex-container" style="margin-top: -20px; padding-left: 4%; margin-bottom: 10px;">
                            <div class="flex-child">
                                <p class="bold_text" style="margin-left: 0;">{transactions[i][0]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-left: 0; font-size: 80%;">{transactions[i][2]}</p>
                            </div>
                            <div class="flex-child" style="text-align: right; margin-bottom: 20px;">
                                <p class="bold_text" style="margin-right: 10%;">{'-' if transactions[i][0] == 'Sent' else '+'} ₺{transactions[i][3]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-right: 10%; font-size: 80%;">{'-' if transactions[i][0] == 'Sent' else '+'} {round((btc_price * float(transactions[i][3])), 6)} BTC</p>
                            </div>
                        </div>
                    </span>
                    """.replace('\n', '')

            else:
                if transactions[i][4] is '':
                    fromatted_base = f"""
                    <span  tabindex="0" class="" role="button" data-toggle="popover" data-trigger="focus" data-placement="top" data-content="{transactions[i][1].strftime('%d-%m-%Y')}">
                        <div name="transaction" class="flex-container" style="margin-top: -20px; padding-left: 4%;">
                            <div class="flex-child">
                                <p class="bold_text" style="margin-left: 0;">{transactions[i][0]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-left: 0; font-size: 80%;">{transactions[i][2]}</p>
                            </div>
                            <div class="flex-child" style="text-align: right; margin-bottom: 20px;">
                                <p class="bold_text" style="margin-right: 10%;">{'-' if transactions[i][0] == 'Sent' else '+'} ₺{transactions[i][3]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-right: 10%; font-size: 80%;">{'-' if transactions[i][0] == 'Sent' else '+'} {round((btc_price * float(transactions[i][3])), 6)} BTC</p>
                            </div>
                        </div>
                    </span>
                    <hr class="dashed">
                    """.replace('\n', '')
                else:
                    fromatted_base = f"""
                    <span  tabindex="0" class="" role="button" data-toggle="popover" data-trigger="focus" data-placement="top" title="{transactions[i][1].strftime('%d-%m-%Y')}" data-content="{transactions[i][4].capitalize()}">
                        <div name="transaction" class="flex-container" style="margin-top: -20px; padding-left: 4%;">
                            <div class="flex-child">
                                <p class="bold_text" style="margin-left: 0;">{transactions[i][0]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-left: 0; font-size: 80%;">{transactions[i][2]}</p>
                            </div>
                            <div class="flex-child" style="text-align: right; margin-bottom: 20px;">
                                <p class="bold_text" style="margin-right: 10%;">{'-' if transactions[i][0] == 'Sent' else '+'} ₺{transactions[i][3]}</p>
                                <p class="dark-text" style="margin-top: -10px; margin-right: 10%; font-size: 80%;">{'-' if transactions[i][0] == 'Sent' else '+'} {round((btc_price * float(transactions[i][3])), 6)} BTC</p>
                            </div>   
                        </div>
                    </span>
                    <hr class="dashed">
                    """.replace('\n', '')
                
            transactions_html += fromatted_base

    return transactions_html