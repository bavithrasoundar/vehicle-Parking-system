from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

vehicles = []

# Helper function to calculate parking charges
def calculate_charge(arrival_time, departure_time):
    time_format = "%H:%M:%S"
    arrival = datetime.strptime(arrival_time, time_format)
    departure = datetime.strptime(departure_time, time_format)
    duration = (departure - arrival).seconds / 3600  # Convert to hours
    return 50 * duration  # Assuming Rs. 50 per hour

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/addVehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    vehicle = {
        "type": "Car" if data['type'] == "1" else "Bike",
        "pltno": data['pltno'],
        "arrive": data['arrive'],
        "date": data['date']
    }
    vehicles.append(vehicle)
    return jsonify({"message": "Vehicle added successfully"}), 201

@app.route('/showVehicles', methods=['GET'])
def show_vehicles():
    return jsonify(vehicles), 200

@app.route('/totalVehicles', methods=['GET'])
def total_vehicles():
    total_cars = len([v for v in vehicles if v['type'] == 'Car'])
    total_bikes = len([v for v in vehicles if v['type'] == 'Bike'])
    return jsonify({"total": len(vehicles), "cars": total_cars, "bikes": total_bikes}), 200


@app.route('/deleteVehicle', methods=['POST'])
def delete_vehicle():
    data = request.json
    for vehicle in vehicles:
        if vehicle['pltno'] == data['pltno'] and vehicle['type'] == ("Car" if data['type'] == "1" else "Bike"):
            charge = calculate_charge(vehicle['arrive'], data['depart'])
            vehicles.remove(vehicle)
            return jsonify({"message": f"Vehicle with number {data['pltno']} has left the parking", "charge": charge}), 200
    return jsonify({"message": "Vehicle not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)