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


class Compass(db.Model):
    __tablename__ = "Compass"
    ID = db.Column(db.Integer, primary_key=True)
    LoadDate = db.Column(db.DateTime)
    DegreesToNorth = db.Column(db.Float())

    def __init__(self,DegreesToNorth):
        self.DegreesToNorth = DegreesToNorth
    def __repr__(self):
        return '' % self.id
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
class Gyroscope(db.Model):
    __tablename__ = "Gyroscope"
    ID = db.Column(db.Integer, primary_key=True)
    LoadDate = db.Column(db.DateTime)
    X = db.Column(db.Float())
    Y = db.Column(db.Float())
    Z = db.Column(db.Float())

    def __init__(self,X,Y,Z):
        self.X = X
        self.Y = Y
        self.Z = Z
    def __repr__(self):
        return '' % self.id
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
class Humidity(db.Model):
    __tablename__ = "Humidity"
    ID = db.Column(db.Integer, primary_key=True)
    LoadDate = db.Column(db.DateTime)
    Humidity = db.Column(db.Float())

    def __init__(self,Humidity):
        self.Humidity = Humidity
    def __repr__(self):
        return '' % self.id
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Orientation(db.Model):
    __tablename__ = "Orientation"
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

class Pressure(db.Model):
    __tablename__ = "Pressure"
    ID = db.Column(db.Integer, primary_key=True)
    LoadDate = db.Column(db.DateTime)
    PressureInHectoPascal = db.Column(db.Float())

    def __init__(self,PressureInHectoPascal):
        self.PressureInHectoPascal = PressureInHectoPascal
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


class CompassSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Compass
        sqla_session = db.session
        load_instance = True

class GyroscopeSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Gyroscope
        sqla_session = db.session
        load_instance = True

class HumiditySchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Humidity
        sqla_session = db.session
        load_instance = True

class OrientationSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Orientation
        sqla_session = db.session
        load_instance = True
    # id = fields.Number(dump_only=True)
    # LoadDate = fields.DateTime(dump_only=True)
    # Temperature = fields.Float(required = True)


class PressureSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Pressure
        sqla_session = db.session
        load_instance = True

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

#region Compass routes
@app.route('/Compass', methods = ['GET'])
def get_comps():
    get_compass = Compass.query.all()
    compass_schema = CompassSchema(many=True)
    compass = compass_schema.dump(get_compass)
    return make_response(jsonify({"Compass": compass}))
@app.route('/Compass/<id>', methods = ['GET'])
def get_comp(id):
    get_compass = Compass.query.get(id)
    compass_schema = CompassSchema(many=False)
    compass = compass_schema.dump(get_compass)
    return make_response(jsonify({"Compass": compass}))
@app.route('/Compass', methods = ['POST'])
def create_comp():
    data = request.get_json()
    comp_schema = CompassSchema()
    comp = comp_schema.load(data,partial=True)
    result = comp_schema.dump(comp.create())
    return make_response(jsonify({"Compass": result}),200)
#endregion

#region Gyroscope routes
@app.route('/Gyroscope', methods = ['GET'])
def get_gyros():
    get_gyroscope = Gyroscope.query.all()
    gyroscope_schema = GyroscopeSchema(many=True)
    gyroscopes = gyroscope_schema.dump(get_gyroscope)
    return make_response(jsonify({"Gyroscope": gyroscopes}))
@app.route('/Gyroscope/<id>', methods = ['GET'])
def get_gyro(id):
    get_gyroscope = Gyroscope.query.get(id)
    gyroscope_schema = GyroscopeSchema(many=False)
    gyroscopes = gyroscope_schema.dump(get_gyroscope)
    return make_response(jsonify({"Gyroscope": gyroscopes}))
@app.route('/Gyroscope', methods = ['POST'])
def create_gryoscope():
    data = request.get_json()
    gyroscope_schema = GyroscopeSchema()
    gyro = gyroscope_schema.load(data,partial=True)
    result = gyroscope_schema.dump(gyro.create())
    return make_response(jsonify({"Gyroscope": result}),200)
#endregion

#region Oritentation routes
@app.route('/Orientation', methods = ['GET'])
def get_oriens():
    get_orientation = Orientation.query.all()
    orientation_schema = OrientationSchema(many=True)
    orientations = orientation_schema.dump(get_orientation)
    return make_response(jsonify({"Orientation": orientations}))
@app.route('/Orientation/<id>', methods = ['GET'])
def get_orien(id):
    get_orientation = Orientation.query.get(id)
    orientation_schema = OrientationSchema(many=False)
    orientations = orientation_schema.dump(get_orientation)
    return make_response(jsonify({"Orientation": orientations}))
@app.route('/Orientation', methods = ['POST'])
def create_orientation():
    data = request.get_json()
    orientation_schema = OrientationSchema()
    orin = orientation_schema.load(data,partial=True)
    result = orientation_schema.dump(orin.create())
    return make_response(jsonify({"Orientation": result}),200)
#endregion

#region Humidity region
@app.route('/Humidity', methods = ['GET'])
def get_hunidities():
    get_humidity = Humidity.query.all()
    humidity_schema = HumiditySchema(many=True)
    humidities = humidity_schema.dump(get_humidity)
    return make_response(jsonify({"Humidity": humidities}))
@app.route('/Humidity/<id>', methods = ['GET'])
def get_Humidity(id):
    get_humidity = Humidity.query.get(id)
    humidity_schema = HumiditySchema(many=False)
    humidities = humidity_schema.dump(get_humidity)
    return make_response(jsonify({"Humidity": humidities}))
@app.route('/Humidity', methods = ['POST'])
def create_humidity():
    data = request.get_json()
    humidity_schema = HumiditySchema()
    humidity = humidity_schema.load(data,partial=True)
    result = humidity_schema.dump(humidity.create())
    return make_response(jsonify({"Humidity": result}),200)
#endregion

#region Humidity region
@app.route('/Pressure', methods = ['GET'])
def get_pressures():
    get_pressure = Pressure.query.all()
    pressure_schema = PressureSchema(many=True)
    pressures = pressure_schema.dump(get_pressure)
    return make_response(jsonify({"Humidity": pressures}))
@app.route('/Pressure/<id>', methods = ['GET'])
def get_pressure(id):
    get_pressure = Pressure.query.get(id)
    pressure_schema = PressureSchema(many=False)
    pressures = pressure_schema.dump(get_pressure)
    return make_response(jsonify({"Pressure": pressures}))
@app.route('/Pressure', methods = ['POST'])
def create_pressure():
    data = request.get_json()
    pressure_schema = PressureSchema()
    pressure = pressure_schema.load(data,partial=True)
    result = pressure_schema.dump(pressure.create())
    return make_response(jsonify({"Humidity": result}),200)
#endregion