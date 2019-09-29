from flask import Flask, jsonify
from flask_restful import reqparse

app = Flask(__name__)
orders_db = []
payments_db = []


class Order:
    # noinspection PyInterpreter
    def __init__(self, id, type, cost, additions):
        self.id = id
        self.type = type
        self.cost = cost
        self.additions = additions
        self.status = "open"
        self.paid = False


class Payment:
    def __init__(self, id, type, amount):
        self.id = id
        self.type = type
        self.amount = amount


class Cash(Payment):
    def __init__(self, id, type, amount):
        Payment.__init__(self, id, type, amount)


class Card(Payment):
    def __init__(self, id, type, amount, card_name, card_no, card_expiry):
        Payment.__init__(self, id, type, amount)
        self.card_name = card_name
        self.card_no = card_no
        self.card_expiry = card_expiry


@app.route("/orders", methods=['POST'])
def create_order():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('type', type=str, required=True)
    parser.add_argument('cost', type=float, required=True)
    parser.add_argument('additions', type=str, action='append')
    args = parser.parse_args()

    id = args.get("id")
    type = args.get("type")
    cost = args.get("cost")
    additions = args["additions"]

    orders_db.append(Order(id, type, cost, additions))
    return jsonify(paymentURL=reqparse.request.base_url + "/" + str(id) + "/payment",
                   orderId=id, orderType=type, orderCost=cost,
                   orderAdditions=additions), 201


@app.route("/orders", methods=['GET'])
def get_orders():
    response = jsonify([order.__dict__ for order in orders_db])
    return response


@app.route("/orders/<status>", methods=['GET'])
def get_orders_by_status(status):
    response = jsonify([order.__dict__ for order in orders_db if order.status == status])
    return response


@app.route("/orders/<int:id>", methods=['GET'])
def get_order(id):
    for order in orders_db:
        if order.id == id:
            return jsonify(order.__dict__)

    return jsonify(id=False), 404


@app.route("/orders/<int:id>", methods=['PATCH'])
def update_order(id):
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('cost', type=float)
    parser.add_argument('additions', type=str, action='append')
    args = parser.parse_args()

    type = args.get("type")
    cost = args.get("cost")
    additions = args["additions"]

    for order in orders_db:
        if order.id == id:
            if order.status != "open":
                return jsonify(orderId=order.id, orderStatus=order.status, error="order is not open"), 403
            if order.paid:
                return jsonify(orderId=order.id, orderPaid=order.paid, error="order is already paid for"), 403
            if type is not None:
                order.type = type
            if cost is not None:
                order.cost = cost
            if additions is not None:
                order.additions = additions
            return jsonify(orderId=order.id, orderType=order.type,
                           orderCost=order.cost, orderAdditions=order.additions), 200

    return jsonify(orderId=False), 404


@app.route("/orders/<int:id>", methods=['DELETE'])
def cancel_order(id):
    for order in orders_db:
        if order.id == id:
            if order.status != "released":
                if not order.paid:
                    orders_db.remove(order)
                    return jsonify(orderId=id, orderType=order.type,
                                   orderCost=order.cost, orderAdditions=order.additions), 200
                return jsonify(orderId=id, orderPaid=order.paid, error="order is already paid for"), 403
            return jsonify(orderId=id, orderStatus=order.status, error="order is already completed"), 403

    return jsonify(orderId=False), 404


@app.route("/orders/<int:id>/prepare", methods=['PATCH'])
def prepare_order(id):
    for order in orders_db:
        if order.id == id:
            if order.status == "open":
                order.status = "preparing"
                return jsonify(orderId=order.id, orderStatus=order.status), 200
            return jsonify(orderId=order.id, orderStatus=order.status, error="order is not open"), 403

    return jsonify(orderId=False), 404


@app.route("/orders/<int:id>/release", methods=['PATCH'])
def release_order(id):
    for order in orders_db:
        if order.id == id:
            if order.status == "preparing":
                if order.paid:
                    order.status = "released"
                    return jsonify(orderId=order.id, orderStatus=order.status,
                                   orderPaid=order.paid), 200
                return jsonify(orderId=order.id, orderPaid=order.paid, error="order is not paid for"), 403
            return jsonify(orderId=order.id, orderStatus=order.status, error="order is not prepared yet"), 403

    return jsonify(orderId=False), 404


@app.route("/orders/<int:id>/payment", methods=['PUT'])
def make_payment(id):
    for payment in payments_db:
        if payment.id == id:
            return jsonify(paymentType=payment.type, paymentAmount=payment.amount,
                           error="payment already made"), 403

    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str, required=True)
    parser.add_argument('amount', type=float, required=True)
    parser.add_argument('card_name', type=str)
    parser.add_argument('card_no', type=int)
    parser.add_argument('card_expiry', type=str)
    args = parser.parse_args()

    type = args.get("type")
    amount = args.get("amount")
    card_name = args.get("card_name")
    card_no = args.get("card_no")
    card_expiry = args.get("card_expiry")

    if type == "cash":
        payments_db.append(Cash(id, type, amount))
        for order in orders_db:
            if order.id == id:
                order.paid = True
        return jsonify(paymentId=id, paymentType=type, paymentAmount=amount), 201
    elif type == "card":
        payments_db.append(Card(id, type, amount, card_name, card_no, card_expiry))
        for order in orders_db:
            if order.id == id:
                order.paid = True
        return jsonify(paymentId=id, paymentType=type,
                       paymentAmount=amount, paymentCardName=card_name,
                       paymentCardNo=card_no, paymentCardExpiry=card_expiry), 201
    else:
        return jsonify(paymentType=type, error="invalid payment type"), 400


@app.route("/orders/<int:id>/payment", methods=['GET'])
def get_payment(id):
    for payment in payments_db:
        if payment.id == id:
            return jsonify(payment.__dict__)

    return jsonify(id=False), 404


if __name__ == '__main__':
    app.run()
