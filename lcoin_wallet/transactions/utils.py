from lcoin_wallet.models import Request, Transaction


def get_sent(current_user):
    sent = Transaction.query.filter_by(by=current_user.username)

    return sent

def check_if_pending(current_user):
    by_user = Request.query.filter_by(by=current_user.username, active=True)
    to_user = Request.query.filter_by(to=current_user.username, active=True)

    return [by_user.first() is not None, to_user.first() is not None], [by_user, to_user]