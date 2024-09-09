# customer.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from App.models import Customer, User, Account
from App.config import db
# from App.utils import admin_required
from datetime import datetime

bp = Blueprint('customer', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    accounts = Account.query.filter_by(customer_id=current_user.customer_id).all()
    return render_template('dashboard.html', accounts=accounts)

@bp.route('/create_customer', methods=['GET', 'POST'])
@login_required
# @admin_required
def create_customer():
    if request.method == 'POST':
        customer = Customer(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d'),
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form['address']
        )
        db.session.add(customer)
        db.session.commit()

        user = User(
            username=request.form['username'],
            customer_id=customer.id
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()

        flash('Customer created successfully')
        return redirect(url_for('customer.dashboard'))
    return render_template('create_customer.html')


# from flask import Blueprint, render_template
# from flask_login import login_required, current_user
# from app.models import Account, Transaction
# from sqlalchemy import desc

# bp = Blueprint('customer', __name__)

# @bp.route('/dashboard')
# @login_required
# def dashboard():
#     accounts = Account.query.filter_by(customer_id=current_user.customer_id).all()
    
#     # Get recent transactions across all accounts
#     recent_transactions = Transaction.query.join(Account).filter(
#         Account.customer_id == current_user.customer_id
#     ).order_by(desc(Transaction.transaction_date)).limit(5).all()
    
#     # Calculate balance after each transaction
#     balance = sum(account.balance for account in accounts)
#     for transaction in reversed(recent_transactions):
#         transaction.balance_after = balance
#         balance -= transaction.amount

#     return render_template('dashboard.html', accounts=accounts, recent_transactions=recent_transactions)