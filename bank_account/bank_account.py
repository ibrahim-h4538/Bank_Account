from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

user_first_name = None
user_last_name = None
user_account_number = None

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class Client(Person):
    def __init__(self, first_name, last_name, account_number, balance=0):
        super().__init__(first_name, last_name)
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount_deposit):
        self.balance += amount_deposit

    def withdrawal(self, amount_withdrawn):
        if self.balance >= amount_withdrawn:
            self.balance -= amount_withdrawn

my_customer = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_first_name, user_last_name, user_account_number, my_customer

    if request.method == 'POST':
        user_first_name = request.form['first_name']
        user_last_name = request.form['last_name']
        user_account_number = request.form['account_number']

        my_customer = Client(user_first_name, user_last_name, user_account_number)

        return redirect(url_for('account'))

    return render_template('login.html')

@app.route('/account')
def account():
    if my_customer:
        return render_template('account.html', user_first_name=user_first_name, user_last_name=user_last_name, user_account_number=user_account_number, client=my_customer)
    else:
        return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])
def deposit():
    amount_deposit = int(request.form['amount'])
    my_customer.deposit(amount_deposit)
    return redirect(url_for('account'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    amount_withdrawn = int(request.form['amount'])
    if amount_withdrawn > my_customer.balance:
        error_message = "Insufficient Funds"
    else:
        my_customer.withdrawal(amount_withdrawn)
        error_message = None
    return render_template('account.html', user_first_name=user_first_name, user_last_name=user_last_name, user_account_number=user_account_number, client=my_customer, error_message=error_message)

@app.route('/')
def index():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
