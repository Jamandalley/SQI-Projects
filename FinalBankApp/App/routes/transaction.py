# transaction.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from App.models import Transaction, Account
from App.config import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('transaction', __name__)

@bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        from_account = Account.query.get(request.form['from_account'])
        to_account = Account.query.filter_by(account_number=request.form['to_account']).first()
        amount = float(request.form['amount'])

        if from_account.customer_id != current_user.customer_id:
            flash('Unauthorized access')
            return redirect(url_for('customer.dashboard'))

        if not to_account:
            flash('Recipient account not found')
            return redirect(url_for('transaction.transfer'))

        if from_account.balance < amount:
            flash('Insufficient funds')
            return redirect(url_for('transaction.transfer'))

        try:
            from_account.balance -= amount
            to_account.balance += amount

            from_transaction = Transaction(
                account_id=from_account.id,
                amount=-amount,
                transaction_type='Transfer',
                description=f"Transfer to {to_account.account_number}"
            )
            to_transaction = Transaction(
                account_id=to_account.id,
                amount=amount,
                transaction_type='Transfer',
                description=f"Transfer from {from_account.account_number}"
            )

            db.session.add(from_transaction)
            db.session.add(to_transaction)
            db.session.commit()

            flash('Transfer successful')
            return redirect(url_for('customer.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.')

    accounts = Account.query.filter_by(customer_id=current_user.customer_id).all()
    return render_template('transfer.html', accounts=accounts)

@bp.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        account = Account.query.get(request.form['account'])
        amount = float(request.form['amount'])

        if account.customer_id != current_user.customer_id:
            flash('Unauthorized access')
            return redirect(url_for('customer.dashboard'))

        try:
            account.balance += amount
            transaction = Transaction(
                account_id=account.id,
                amount=amount,
                transaction_type='Deposit',
                description="Cash deposit"
            )
            db.session.add(transaction)
            db.session.commit()

            flash('Deposit successful')
            return redirect(url_for('customer.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.')

    accounts = Account.query.filter_by(customer_id=current_user.customer_id).all()
    return render_template('deposit.html', accounts=accounts)

@bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        account = Account.query.get(request.form['account'])
        amount = float(request.form['amount'])

        if account.customer_id != current_user.customer_id:
            flash('Unauthorized access')
            return redirect(url_for('customer.dashboard'))

        if account.balance < amount:
            flash('Insufficient funds')
            return redirect(url_for('transaction.withdraw'))

        try:
            account.balance -= amount
            transaction = Transaction(
                account_id=account.id,
                amount=-amount,
                transaction_type='Withdrawal',
                description="Cash withdrawal"
            )
            db.session.add(transaction)
            db.session.commit()

            flash('Withdrawal successful')
            return redirect(url_for('customer.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.')

    accounts = Account.query.filter_by(customer_id=current_user.customer_id).all()
    return render_template('withdraw.html', accounts=accounts)

@bp.route('/transaction_history')
@login_required
def transaction_history():
    accounts = Account.query.filter_by(customer_id=current_user.customer_id).all()
    transactions = Transaction.query.join(Account).filter(Account.customer_id == current_user.customer_id).order_by(Transaction.transaction_date.desc()).limit(50).all()
    return render_template('transaction_history.html', transactions=transactions, accounts=accounts)
