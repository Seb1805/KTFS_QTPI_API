from flask import Flask, request, jsonify, make_response, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from datetime import datetime
from sqlalchemy import cast, DateTime, Date
import graph.graph_temp as p_temp
import graph.graph_accelerometer as acc_m 
#from graph/graph_temp import plot_to_img as pti


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://pyUser:password@192.168.3.213:3306/SensorData'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.json.sort_keys = False


from urllib.parse import urlparse, parse_qs




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

    def __init__(self, Temperature):
        self.Temperature = Temperature

    def __repr__(self):
        return f"Temperature(ID={self.ID}, LoadDate={self.LoadDate}, Temperature={self.Temperature})"

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
# @app.route('/Temperature/date', methods = ['GET'])
# def get_temp_by_date():
#     print(request.url)


#     # Parse the URL
#     parsed_url = urlparse(request.url)

#     # Get the query string
#     query_string = parsed_url.query

#     # Parse the query string and get the parameters as a dictionary
#     parameters = parse_qs(query_string)
#     x_date = parameters.get("LoadDate",[""])[0]
#     print(x_date)
#     print(Temperature.LoadDate)
#     #load_date = request.args.get('LoadDate')  # Assuming 'LoadDate' is the parameter to filter by
#     x_date = x_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time

#     temperatures = Temperature.query.filter(cast(Temperature.LoadDate, Date) >= datetime.strptime(x_date, '%Y-%m-%d %H:%M:%S')).all()

#     temperature_schema = TemperatureSchema(many=True)
#     temperatures_json = temperature_schema.dump(temperatures)

#     return make_response(jsonify({"Temperature": temperatures_json}))
@app.route('/Temperature/date', methods=['GET'])
def get_temp_by_date():
    load_date = None
    load_end_date = None
    if(request.args.get('LoadDate') != None):
        load_date = request.args.get('LoadDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_date = load_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    
    if(request.args.get('LoadEndDate') != None):
        load_end_date = request.args.get('LoadEndDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_end_date = load_end_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    # Print sample values of LoadDate column
    sample_dates = Temperature.query.with_entities(Temperature.LoadDate).limit(5).all()

    #temperatures = Temperature.query.filter(cast(Temperature.LoadDate, Date) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
    
    if(load_date or load_end_date):
        if(load_date):
            load_date = datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')
        else:
            load_date = datetime.strptime("1940-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        if(load_end_date): 
            load_end_date = datetime.strptime(load_end_date, '%Y-%m-%d %H:%M:%S')
        else: 
            load_end_date = cast(datetime.now(), DateTime)
        # - startdate - enddate - startdate&enddate
        # temperatures = Temperature.query.filter(cast(Temperature.LoadDate, DateTime) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
        # temperatures = Temperature.query.filter(load_date < load_end_date).all()
        temperatures = Temperature.query.filter(load_date < cast(Temperature.LoadDate, DateTime), 
        cast(Temperature.LoadDate, DateTime) < load_end_date).all()

        print(load_date)
        print(load_end_date)
        print(load_date < load_end_date)


        temperature_schema = TemperatureSchema(many=False)
        temperatures_json = temperature_schema.dump(temperatures)

        #return make_response(jsonify({"Temperature": temperatures_json}))
        temperatures_dict = [temperature_schema.dump(temperature) for temperature in temperatures]
        return make_response(jsonify({"Temperature": temperatures_dict}))
    return make_response(jsonify({"Temperature": None}),404)

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
    return make_response(jsonify({"Accelerometer": result}),200)
@app.route('/Accelerometer/date', methods=['GET'])
def get_accelerometer_by_date():
    load_date = None
    load_end_date = None
    if(request.args.get('LoadDate') != None):
        load_date = request.args.get('LoadDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_date = load_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    
    if(request.args.get('LoadEndDate') != None):
        load_end_date = request.args.get('LoadEndDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_end_date = load_end_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    # Print sample values of LoadDate column
    #sample_dates = Temperature.query.with_entities(Hunidity.LoadDate).limit(5).all()

    #temperatures = Temperature.query.filter(cast(Temperature.LoadDate, Date) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
    
    if(load_date or load_end_date):
        if(load_date):
            load_date = datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')
        else:
            load_date = datetime.strptime("1940-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        if(load_end_date): 
            load_end_date = datetime.strptime(load_end_date, '%Y-%m-%d %H:%M:%S')
        else: 
            load_end_date = cast(datetime.now(), DateTime)
        # - startdate - enddate - startdate&enddate
        # temperatures = Temperature.query.filter(cast(Temperature.LoadDate, DateTime) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
        # temperatures = Temperature.query.filter(load_date < load_end_date).all()
        temperatures = Accelerometer.query.filter(load_date < cast(Accelerometer.LoadDate, DateTime), 
        cast(Accelerometer.LoadDate, DateTime) < load_end_date).all()

        print(load_date)
        print(load_end_date)
        print(load_date < load_end_date)


        accelerometer_schema = AccelerometerSchema(many=False)
        temperatures_json = accelerometer_schema.dump(temperatures)

        #return make_response(jsonify({"Temperature": temperatures_json}))
        temperatures_dict = [accelerometer_schema.dump(temperature) for temperature in temperatures]
        return make_response(jsonify({"Accelerometer": temperatures_dict}))
    return make_response(jsonify({"Accelerometer": None}),404)

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
@app.route('/Compass/date', methods=['GET'])
def get_compass_by_date():
    load_date = None
    load_end_date = None
    if(request.args.get('LoadDate') != None):
        load_date = request.args.get('LoadDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_date = load_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    
    if(request.args.get('LoadEndDate') != None):
        load_end_date = request.args.get('LoadEndDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_end_date = load_end_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    # Print sample values of LoadDate column
    #sample_dates = Temperature.query.with_entities(Hunidity.LoadDate).limit(5).all()

    #temperatures = Temperature.query.filter(cast(Temperature.LoadDate, Date) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
    
    if(load_date or load_end_date):
        if(load_date):
            load_date = datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')
        else:
            load_date = datetime.strptime("1940-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        if(load_end_date): 
            load_end_date = datetime.strptime(load_end_date, '%Y-%m-%d %H:%M:%S')
        else: 
            load_end_date = cast(datetime.now(), DateTime)
        # - startdate - enddate - startdate&enddate
        # temperatures = Temperature.query.filter(cast(Temperature.LoadDate, DateTime) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
        # temperatures = Temperature.query.filter(load_date < load_end_date).all()
        temperatures = Compass.query.filter(load_date < cast(Compass.LoadDate, DateTime), 
        cast(Compass.LoadDate, DateTime) < load_end_date).all()

        print(load_date)
        print(load_end_date)
        print(load_date < load_end_date)


        compass_schema = CompassSchema(many=False)
        temperatures_json = compass_schema.dump(temperatures)

        #return make_response(jsonify({"Temperature": temperatures_json}))
        temperatures_dict = [compass_schema.dump(temperature) for temperature in temperatures]
        return make_response(jsonify({"Compass": temperatures_dict}))
    return make_response(jsonify({"Compass": None}),404)
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
@app.route('/Humidity/date', methods=['GET'])
def get_humidity_by_date():
    load_date = None
    load_end_date = None
    if(request.args.get('LoadDate') != None):
        load_date = request.args.get('LoadDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_date = load_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    
    if(request.args.get('LoadEndDate') != None):
        load_end_date = request.args.get('LoadEndDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_end_date = load_end_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    # Print sample values of LoadDate column
    #sample_dates = Temperature.query.with_entities(Hunidity.LoadDate).limit(5).all()

    #temperatures = Temperature.query.filter(cast(Temperature.LoadDate, Date) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
    
    if(load_date or load_end_date):
        if(load_date):
            load_date = datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')
        else:
            load_date = datetime.strptime("1940-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        if(load_end_date): 
            load_end_date = datetime.strptime(load_end_date, '%Y-%m-%d %H:%M:%S')
        else: 
            load_end_date = cast(datetime.now(), DateTime)
        # - startdate - enddate - startdate&enddate
        # temperatures = Temperature.query.filter(cast(Temperature.LoadDate, DateTime) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
        # temperatures = Temperature.query.filter(load_date < load_end_date).all()
        temperatures = Humidity.query.filter(load_date < cast(Humidity.LoadDate, DateTime), 
        cast(Humidity.LoadDate, DateTime) < load_end_date).all()

        print(load_date)
        print(load_end_date)
        print(load_date < load_end_date)


        humidity_schema = HumiditySchema(many=False)
        temperatures_json = humidity_schema.dump(temperatures)

        #return make_response(jsonify({"Temperature": temperatures_json}))
        temperatures_dict = [humidity_schema.dump(temperature) for temperature in temperatures]
        return make_response(jsonify({"Humidity": temperatures_dict}))
    return make_response(jsonify({"Humidity": None}),404)

#endregion

#region Humidity region
@app.route('/Pressure', methods = ['GET'])
def get_pressures():
    get_pressure = Pressure.query.all()
    pressure_schema = PressureSchema(many=True)
    pressures = pressure_schema.dump(get_pressure)
    return make_response(jsonify({"Pressure": pressures}))
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
    return make_response(jsonify({"Pressure": result}),200)
@app.route('/Pressure/date', methods=['GET'])
def get_pressure_by_date():
    load_date = None
    load_end_date = None
    if(request.args.get('LoadDate') != None):
        load_date = request.args.get('LoadDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_date = load_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    
    if(request.args.get('LoadEndDate') != None):
        load_end_date = request.args.get('LoadEndDate')  # Assuming 'LoadDate' is the parameter to filter by
        load_end_date = load_end_date.replace('T', ' ')  # Replace 'T' with a space to separate date and time
    # Print sample values of LoadDate column
    #sample_dates = Temperature.query.with_entities(Hunidity.LoadDate).limit(5).all()

    #temperatures = Temperature.query.filter(cast(Temperature.LoadDate, Date) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
    
    if(load_date or load_end_date):
        if(load_date):
            load_date = datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')
        else:
            load_date = datetime.strptime("1940-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        if(load_end_date): 
            load_end_date = datetime.strptime(load_end_date, '%Y-%m-%d %H:%M:%S')
        else: 
            load_end_date = cast(datetime.now(), DateTime)
        # - startdate - enddate - startdate&enddate
        # temperatures = Temperature.query.filter(cast(Temperature.LoadDate, DateTime) >= datetime.strptime(load_date, '%Y-%m-%d %H:%M:%S')).all()
        # temperatures = Temperature.query.filter(load_date < load_end_date).all()
        temperatures = Pressure.query.filter(load_date < cast(Pressure.LoadDate, DateTime), 
        cast(Pressure.LoadDate, DateTime) < load_end_date).all()

        print(load_date)
        print(load_end_date)
        print(load_date < load_end_date)


        pressure_schema = PressureSchema(many=False)
        temperatures_json = pressure_schema.dump(temperatures)

        #return make_response(jsonify({"Temperature": temperatures_json}))
        temperatures_dict = [pressure_schema.dump(temperature) for temperature in temperatures]
        return make_response(jsonify({"Pressure": temperatures_dict}))
    return make_response(jsonify({"Pressure": None}),404)
#endregion

#region plot
@app.route('/plot')
def plot():
    img_b64 = p_temp.plot_to_img()

    html = f'<img src ="data:image/png;base64,{img_b64}" class="blog-image">'
    return render_template_string(html)




#endregion