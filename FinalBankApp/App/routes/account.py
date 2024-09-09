# account.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from App.models import Account
from App.config import db
import random

bp = Blueprint('account', __name__)

@bp.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account():
    if request.method == 'POST':
        account = Account(
            customer_id=current_user.customer_id,
            account_type=request.form['account_type'],
            account_number=f"4{random.randint(100000000, 999999999)}",
            balance=0
        )
        
        db.session.add(account)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('customer.dashboard'))
    return render_template('create_account.html')

@bp.route('/check_balance/<account_id>')
@login_required
def check_balance(account_id):
    account = Account.query.get_or_404(account_id)
    if account.customer_id != current_user.customer_id:
        flash('Unauthorized access')
        return redirect(url_for('customer.dashboard'))
    return render_template('check_balance.html', account=account)