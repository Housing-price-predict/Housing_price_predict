import requests
from flask import Flask, flash, redirect, render_template, request, session, abort


def try_1(room, type, method, field, regionname, distance, bedroom, bathroom, car, number):
    params = {"username": "admin", "password": "admin"}
    url = "http://0.0.0.0:9321/token"
    r = requests.get(url, params)
    token = r.json()['token']
    print(r.json())
    headers = {'AUTH-TOKEN': token}
    params = {"Landsize": number, "Car": car, "Bathroom": bathroom, "Bedroom": bedroom, "Distance": distance,
              "Regionname": regionname, "Field": field, "Method": method, "Type": type,
              "Rooms": room}
    url = "http://0.0.0.0:9321/product_predict"
    r = requests.get(url, headers = headers, params = params)
    print(r.json())
    return r.text

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print(request.form)
        room = request.form['room']
        type = request.form['type']
        method = request.form['method']
        field = request.form['field']
        regionname = request.form['regionname']
        distance = request.form['distance']
        bedroom = request.form['bedroom']
        bathroom = request.form['bathroom']
        car = request.form['car']
        number = request.form['number']
        #result = try_1(room, type, method, field, regionname, distance, bedroom, bathroom, car, number)
        if room:
            dict_room = try_1(room, type, method, field, regionname, distance, bedroom, bathroom, car, number)

        else:
            result = try_1(0, type, method, field, regionname, distance, bedroom, bathroom, car, number)
        return result
    return render_template('ui1.html')


if __name__ == '__main__':
    app.run(debug=True)
