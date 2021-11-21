from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

# from sqlalchemy import Column, Integer, String
local_server = True
app = Flask(__name__)
app.secret_key = 'big_secret'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/railway_db'
db = SQLAlchemy(app)
db.init_app(app)


class Train(db.Model):
    __tablename__ ='train'
    train_id = db.Column('train_id',db.Integer, primary_key=True)
    track_id = db.Column('track_id', db.Integer)

    def __init__(self, train_id, track_id):
        self.train_id = train_id
        self.track_id = track_id


class Station(db.Model):
    __tablename__ = 'station'
    station_id = db.Column('station_id', db.Integer, primary_key=True)
    track_id = db.Column('track_id', db.Integer)

    def __init__(self, track_id, station_id):
        self.station_id = station_id
        self.track_id = track_id


class Schedule(db.Model):
    __tablename__ = 'schedule'
    station_id = db.Column('station_id', db.Integer, primary_key=True)
    train_id = db.Column('train_id', db.Integer, primary_key=True)
    arrival_time = db.Column('arrival_time')
    departure_time = db.Column('arrival_time')

    def __init__(self, station_id, train_id, arrival_time, departure_time):
        self.train_id = train_id
        self.station_id = station_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/train/add", methods=['POST','GET'])
def train_add():
    if request.method == 'POST':
        train_id = int(request.form['TRAIN_ID'])
        track_id = int(request.form['TRACK_ID'])
        if train_id != '' and track_id != '':
            new_record = Train(train_id, track_id)
            db.session.add(new_record)
            db.session.commit()
            result = "Record added successfully."
        else:
            result = "Input Needed."
        return render_template('train.html',result=result)
    return render_template('train.html')



@app.route("/train/delete", methods=['POST','GET'])
def train_delete():
    if request.method == 'POST':
        train_id = int(request.form['TRAIN_ID'])
        if train_id != '' :
            delete_record = Train.query.filter_by(train_id=train_id).first()
            db.session.delete(delete_record)
            db.session.commit()
            result = "Record Deleted successfully."
        else:
            result = "Input Needed."
        return render_template('train.html', result=result)
    return render_template('train.html')


@app.route("/train/update", methods=['POST','GET'])
def train_update():
    if request.method == 'POST':
        train_id = int(request.form['TRAIN_ID'])
        track_id = int(request.form['TRACK_ID'])
        if train_id != '' and track_id != '':
            update_record = Train.query.filter_by(train_id=train_id).first()
            update_record.track_id = track_id
            db.session.commit()
            result = "Record updated successfully."
        else:
            result = "Input Needed."
        return render_template('train.html', result=result)
    return render_template('train.html')


@app.route("/station/add", methods=['POST','GET'])
def station_add():
    if request.method == 'POST':
        station_id = int(request.form['STATION_ID'])
        track_id = int(request.form['TRACK_ID'])
        if station_id != '' and track_id != '' :
            new_record = Station(track_id, station_id)
            db.session.add(new_record)
            db.session.commit()
            result = "Record added successfully."
        else:
            result = "Input Needed."
        return render_template('station.html', result=result)
    return render_template('station.html')


@app.route("/station/delete", methods=['POST','GET'])
def station_delete():
    if request.method == 'POST':
        station_id = int(request.form['STATION_ID'])
        if station_id != '' :
            delete_record = Station.query.filter_by(station_id=station_id).first()
            db.session.delete(delete_record)
            db.session.commit()
            result = "Record deleted successfully."
        else:
            result = "Input Needed."
        return render_template('station.html', result=result)
    return render_template('station.html')

@app.route("/station/update", methods=['POST','GET'])
def station_update():
    if request.method == 'POST':
        track_id = int(request.form['TRACK_ID'])
        station_id = int(request.form['STATION_ID'])
        if station_id != '' and track_id != '' :
            update_record = Station.query.filter_by(station_id=station_id).first()
            update_record.track_id = track_id
            db.session.commit()
            result = "Record updated successfully."
        else:
            result = "Input Needed."
        return render_template('station.html', result=result)
    return render_template('station.html')


@app.route("/schedule/add", methods=['POST','GET'])
def schedule_add():
    if request.method == 'POST':
        train_id = int(request.form['TRAIN_ID'])
        station_id = int(request.form['STATION_ID'])
        arrival_time = request.form['ARRIVAL_TIME']
        departure_time = request.form['DEPARTURE_TIME']
        if station_id != '' and train_id != '' and arrival_time != '' and departure_time != '' :

            #new_record = Schedule(station_id=station_id, train_id=train_id, arrival_time=arrival_time,
              #                    departure_time=departure_time)
            #db.session.add(new_record)
            #db.session.commit()
            #sql = "INSERT INTO schedule(train_id,station_id,arrival_time,departure_time) " \
             #     "VALUES(train_id,station_id,arrival_time,departure_time);"
            db.engine.execute(sql)
            result = "Record added successfully."
        else:
            result = "Input Needed."
        return render_template('schedule.html', result=result)
    return render_template('schedule.html')


@app.route("/schedule/delete", methods=['POST','GET'])
def schedule_delete():
    if request.method == 'POST':
        train_id = int(request.form['TRAIN_ID'])
        station_id = int(request.form['STATION_ID'])
        if station_id != '' and train_id != '' :
            delete_record = Schedule.query.filter_by(station_id=station_id, train_id=train_id).first()
            if delete_record is None:
                result = "No such record was found."
            else:
                db.session.commit()
                result = "Record deleted successfully."
                db.session.delete(delete_record)
        else:
            result = "Input Needed."
        return render_template('schedule.html', result=result)
    return render_template('schedule.html')


@app.route("/schedule/update", methods=['POST','GET'])
def schedule_update():
    if request.method == 'POST':
        train_id = int(request.form['TRAIN_ID'])
        station_id = int(request.form['STATION_ID'])
        arrival_time = request.form['ARRIVAL_TIME']
        departure_time = request.form['DEPARTURE_TIME']
        if  station_id != '' and train_id != '' :
            update_record = Schedule.query.filter(Schedule.train_id == train_id,
                                                  Schedule.station_id == station_id).first()
            if update_record == None:
                result = "No such record was not found."
            update_record.arrival_time = arrival_time
            update_record.departure_time = departure_time
            db.session.commit()
            result = "Record Upadted successfully."
        else:
            result = "Input Needed."
        return render_template('schedule.html', result=result)
    return render_template('schedule.html')

@app.route("/user", methods=['POST','GET'])
def user():
    if request.method == 'POST':
        train_id = int(request.form.get('TRAIN_ID'))
        if train_id != '' :
            sql = "SELECT station_id,arrival_time,departure_time FROM schedule WHERE train_id=" + str(
                train_id) + " ORDER BY station_id DESC"
            data = db.engine.execute(sql).fetchall()
            result = data
        else:
            result = 'Input needed.'
        return render_template('user.html',result=result)
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)
