from App.models import Account, db

def process_transaction(form_data):
    from_account = Account.query.filter_by(account_number=form_data['from_account']).first()
    to_account = Account.query.filter_by(account_number=form_data['to_account']).first()

    if from_account and to_account and from_account.balance >= float(form_data['amount']):
        from_account.balance -= float(form_data['amount'])
        to_account.balance += float(form_data['amount'])
        db.session.commit()
        return True
    return False
