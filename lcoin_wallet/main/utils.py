from lcoin_wallet.models import Request, Transaction

from lcoin_wallet.models import Transaction, Request

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
                    transaction.to, transaction.amount])

    for transaction in received_:
        received.append(["Received", transaction.date,
                        transaction.by, transaction.amount])

    lists = sorted(sent + received, key=lambda x: x[1])

    return lists