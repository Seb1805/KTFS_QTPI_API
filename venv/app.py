from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://pyUser:password@192.168.3.213:3306/SensorData'
db = SQLAlchemy(app)
ma = Marshmallow(app)


###Models####

#region Produkt eksempel
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    productDescription = db.Column(db.String(100))
    productBrand = db.Column(db.String(20))
    price = db.Column(db.Integer)

    def __init__(self,title,productDescription,productBrand,price):
        self.title = title
        self.productDescription = productDescription
        self.productBrand = productBrand
        self.price = price
    def __repr__(self):
        return '' % self.id

    def create(self):
    #   with app.app_context():
        db.session.add(self)
        db.session.commit()
        return self
#endregion


class Temperature(db.Model):
    __tablename__ = "Temperature"
    ID = db.Column(db.Integer, primary_key=True)
    LoadDate = db.Column(db.DateTime)
    Temperature = db.Column(db.Float())

    def __init__(self,Temperature):
        self.Temperature = Temperature
    def __repr__(self):
        return '' % self.id
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Accelerometer(db.Model):
    __tablename__ = "Accelerometer"
    ID = db.Column(db.Integer, primary_key=True)
    LoadDate = db.Column(db.DateTime)
    Pitch = db.Column(db.Float())
    Roll = db.Column(db.Float())
    Yaw = db.Column(db.Float())

    def __init__(self,Pitch,Roll,Yaw):
        self.Pitch = Pitch
        self.Roll = Roll
        self.Yaw = Yaw
    def __repr__(self):
        return '' % self.id
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    




# with app.app_context():
#     db.create_all()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    productDescription = fields.String(required=True)
    productBrand = fields.String(required=True)
    price = fields.Number(required=True)

class TemperatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Temperature
        sqla_session = db.session
        load_instance = True


class AccelerometerSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Accelerometer
        sqla_session = db.session
        load_instance = True


    # id = fields.Number(dump_only=True)
    # LoadDate = fields.DateTime(dump_only=True)
    # Temperature = fields.Float(required = True)




# @app.route('/products', methods = ['GET'])
# def index():
#     get_products = Product.query.all()
#     product_schema = ProductSchema(many=True)
#     products = product_schema.dump(get_products)
#     return make_response(jsonify({"product": products}))

#region Temperature routes
@app.route('/Temperature', methods = ['GET'])
def get_temps():
    get_temperature = Temperature.query.all()
    temperature_schema = TemperatureSchema(many=True)
    temperatures = temperature_schema.dump(get_temperature)
    return make_response(jsonify({"Temperature": temperatures}))
@app.route('/Temperature/<id>', methods = ['GET'])
def get_temp(id):
    get_temperature = Temperature.query.get(id)
    temperature_schema = TemperatureSchema(many=False)
    temperatures = temperature_schema.dump(get_temperature)
    return make_response(jsonify({"Temperature": temperatures}))
@app.route('/Temperature', methods = ['POST'])
def create_temperature():
    data = request.get_json()
    temp_schema = TemperatureSchema()
    temp = temp_schema.load(data,partial=True)
    result = temp_schema.dump(temp.create())
    return make_response(jsonify({"Temperature": result}),200)
#endregion

#region Accelerometer routes
@app.route('/Accelerometer', methods = ['GET'])
def get_accels():
    get_accelerometer = Accelerometer.query.all()
    accelerometer_schema = AccelerometerSchema(many=True)
    accelerometers = accelerometer_schema.dump(get_accelerometer)
    return make_response(jsonify({"Accelerometer": accelerometers}))
@app.route('/Accelerometer/<id>', methods = ['GET'])
def get_accel(id):
    get_accelerometer = Accelerometer.query.get(id)
    accelerometer_schema = AccelerometerSchema(many=False)
    accelerometers = accelerometer_schema.dump(get_accelerometer)
    return make_response(jsonify({"Accelerometer": accelerometers}))
@app.route('/Accelerometer', methods = ['POST'])
def create_accelerometer():
    data = request.get_json()
    accelerometer_schema = AccelerometerSchema()
    temp = accelerometer_schema.load(data,partial=True)
    result = accelerometer_schema.dump(temp.create())
    return make_response(jsonify({"Temperature": result}),200)
#endregion


@app.route('/products', methods = ['GET'])
def index():
    get_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    products = product_schema.dump(get_products)
    return make_response(jsonify({"product": products}))
@app.route('/products', methods = ['POST'])
def create_product():
    data = request.get_json()
    # product_schema = ProductSchema()
    # product = product_schema.load(data)
    # result = product_schema.dump(product.create())
    return make_response(jsonify({"product": data}),200)