from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
logging.basicConfig(
    filename='app_log.log',
    level=logging.WARNING,
    format='%(asctime)s.%(msecs)03d : %(levelname)s : %(module)s - %(funcName)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
db = SQLAlchemy(app)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(100), nullable=False, unique=True)
    menu_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Menu('{self.menu_name}', '{self.menu_price}')"


@app.get("/")
def index():
    return render_template('index.html')


@app.get("/menu")
def menu():
    all_menus = Menu.query.all()
    return render_template('menu.html', all_menus=all_menus)


@app.get("/add-menu")
def add_menu():
    return render_template('add-menu.html')


@app.post("/save-menu")
def save_menu():
    menu_name = request.form.get("menu_name")
    menu_price = request.form.get("menu_price")
    new_menu_item = Menu(menu_name=menu_name, menu_price=menu_price)
    try:
        db.session.add(new_menu_item)
        db.session.commit()
    except IntegrityError as ie:
        message = f"{menu_name} is already exist, UNIQUE constraint failed"
        flash(message, "Error")
        app.logger.error(message)
    except Exception as ex:
        print(ex.args)
    return redirect(url_for("menu"))


@app.post("/new-customer")
def new_customer():
    customer_name = request.form.get("customer_name")
    phone_number = request.form.get("phone_number")
    customer = {"customer_name": customer_name, "phone_number": phone_number}
    all_menus = Menu.query.all()
    return render_template('order.html', customer=customer, all_menus=all_menus)


@app.post("/print-order")
def print_order():
    user_order = {}
    customer_name = request.form.get("customer_name")
    phone_number = request.form.get("phone_number")
    user_order.update({"customer_name": customer_name, "phone_number": phone_number})
    total_amount = 0
    order_list = []
    selected_items = request.form.getlist('items')
    for selected_item in selected_items:
        menu_name, menu_price = selected_item.split("##")
        order_list.append({"menu_name": menu_name, "menu_price": menu_price, })
        total_amount += float(menu_price)
    user_order.update({"order_list": order_list, "total_amount": total_amount, })
    return render_template('order-details.html', user_order=user_order)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8181, debug=True)
