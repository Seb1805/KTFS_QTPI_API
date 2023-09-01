from flask import Flask, request, jsonify, make_response, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow
from marshmallow import fields
from datetime import datetime
from sqlalchemy import cast, DateTime, Date
import graph.graph_temp as p_temp
import graph.graph_accelerometer as graphAccelerometer
# import graph.graph_humidity as graphHumidity
# import graph.graph_pressure as graphPressure
import graph.graph_compass as graphCompass
#from graph/graph_temp import plot_to_img as pti


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://pyUser:password@192.168.3.213:3306/SensorData'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.json.sort_keys = False


from urllib.parse import urlparse, parse_qs




#region Models

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

    def getName(self):
        return __tablename__
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

#endregion

# with app.app_context():
#     db.create_all()

#region Schemas
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


class PressureSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Pressure
        sqla_session = db.session
        load_instance = True
#endregion

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
@app.route('/Temperature/date', methods=['GET'])
def get_temp_by_date():
    graph = GenerateDataDateRange(TemperatureSchema, Temperature, request.args.get('StartDate'), request.args.get('EndDate'))
    if(graph == None):
        return make_response(jsonify({}),404)
    
    else:
        return make_response(graph)
    

@app.route('/Temperature/plot')
async def get_temperature_plot():
    img_b64 = await p_temp.main('Temperature')

    html = f'<img src ="data:image/png;base64,{img_b64}" class="blog-image">'
    if img_b64:
        del img_b64
    return render_template_string(html)




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
@app.route('/Accelerometer/date', methods=['GET'])
def get_accelerometer_by_date():
    graph = GenerateDataDateRange(AccelerometerSchema, Accelerometer, request.args.get('StartDate'), request.args.get('EndDate'))
    if(graph == None):
        return make_response(jsonify({}),404)
    
    else:
        return make_response(graph)


@app.route('/Accelerometer', methods = ['POST'])
def create_accelerometer():
    data = request.get_json()
    accelerometer_schema = AccelerometerSchema()
    temp = accelerometer_schema.load(data,partial=True)
    result = accelerometer_schema.dump(temp.create())
    return make_response(jsonify({"Accelerometer": result}),200)

@app.route('/Accelerometer/plot')
async def get_accelerometer_plot():
    img_b64 = await graphAccelerometer.main()

    html = f'<img src ="data:image/png;base64,{img_b64}" class="blog-image">'
    if img_b64:
        del img_b64
    return render_template_string(html)


#endregion

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
    graph = GenerateDataDateRange(CompassSchema, Compass, request.args.get('StartDate'), request.args.get('EndDate'))
    if(graph == None):
        return make_response(jsonify({}),404)
    
    else:
        return make_response(graph)
    
@app.route('/Compass/plot')
async def get_compass_plot():
    img_b64 = await p_temp.main('Compass', 'DegreesToNorth')

    html = f'<img src ="data:image/png;base64,{img_b64}" class="blog-image">'
    if img_b64:
        del img_b64
    return render_template_string(html)

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

#region Humidity routes
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
    graph = GenerateDataDateRange(HumiditySchema, Humidity, request.args.get('StartDate'), request.args.get('EndDate'))
    if(graph == None):
        return make_response(jsonify({}),404)
    
    else:
        return make_response(graph)
@app.route('/Humidity/plot')
async def plot():
    img_b64 = await p_temp.main('Humidity')

    html = f'<img src ="data:image/png;base64,{img_b64}" class="blog-image">'
    if img_b64:
        del img_b64
    return render_template_string(html)

#endregion

#region Pressure routes
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
    graph = GenerateDataDateRange(PressureSchema, Pressure, request.args.get('StartDate'), request.args.get('EndDate'))
    if(graph == None):
        return make_response(jsonify({}),404)
    
    else:
        return make_response(graph)
    
@app.route('/Pressure/plot')
async def get_pressure_plot():
    img_b64 = await p_temp.main('Pressure')

    html = f'<img src ="data:image/png;base64,{img_b64}" class="blog-image">'
    if img_b64:
        del img_b64
    return render_template_string(html)

#endregion


#region HelperFunctions
def GenerateDataDateRange(schema, chosenClass, startDate = None, endDate = None):
    # Replace 'T' with a space to separate date and time
    if(startDate != None):
        startDate = startDate.replace('T', ' ')
    
    # Replace 'T' with a space to separate date and time
    if(endDate != None):
        endDate = endDate.replace('T', ' ')

    # Check if either startDate or endDate is provided
    if(startDate or endDate):
        # If startDate is provided, convert it to datetime object
        # Otherwise, set it to a default value of 1940-01-01 00:00:00
        if(startDate):
            startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        else:
            startDate = datetime.strptime("1940-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        
        # If endDate is provided, convert it to datetime object
        # Otherwise, set it to the current datetime
        if(endDate): 
            endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        else: 
            endDate = cast(datetime.now(), DateTime)

        # Filter the data based on the date range
        filteredData = chosenClass.query.filter(startDate < cast(chosenClass.LoadDate, DateTime), 
                       cast(chosenClass.LoadDate, DateTime) < endDate).all()

        # Create a schema object and dump the filtered data into a dictionary
        created_schema = schema(many=False)
        created_dict = [created_schema.dump(temperature) for temperature in filteredData]

        # Return the filtered data as a JSON object
        return jsonify({chosenClass.__tablename__ : created_dict})
    else: 
        # If neither startDate nor endDate is provided, return an empty JSON object
        return jsonify()
    
#endregion