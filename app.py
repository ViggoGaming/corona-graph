__version__ = 2.0

import requests, json, datetime
from flask import Flask, render_template, url_for, jsonify, request, redirect, session
from flask_googlecharts import GoogleCharts, MaterialLineChart

BASE_URL = "https://pomber.github.io/covid19/timeseries.json"

countries = ["Denmark", "Norway", "Sweden", "Afghanistan"]
app = Flask(__name__)
app.secret_key = "key"
charts = GoogleCharts(app)

r = requests.get(BASE_URL).json()

datalength = len([x["date"] for x in r[countries[0]]])

@app.route('/', methods=["GET", "POST"])
def index():
    zoom=session.get('zoom') if session.get('zoom') != None else 31
    if request.method == "POST":
        zoom = int(request.form.get("slider"))
    dates = [x["date"] for x in r[countries[0]]][-zoom:] # Make sure if length is not the same to: Improve to find date of longest country data
    corona_chart = MaterialLineChart("corona", options={"title": "Corona chart", "width": 1200, "height": 800})
    corona_chart.add_column("string", "Date")
    for country in countries:
        corona_chart.add_column("number", country)
    for i, date in enumerate(dates):
        row_data = [date]
        for country in countries:
            row_data.append([j["deaths"]-x["deaths"] for x,j in zip(r[country], r[country][1:])][-zoom:][i])
        corona_chart.add_rows([row_data])
    charts.register(corona_chart)
    session['zoom'] = zoom
    return render_template('index.html', datalength=datalength-2, zoom=zoom, countries=countries)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
