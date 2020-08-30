from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))



@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        Journey_weekday = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").dayofweek)

        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)

        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)

        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        Total_stops = int(request.form["stops"])

        airline=request.form['airline']
        airlines_row = np.zeros(11, dtype=int)
        if airline == 'Air India':
            airlines_row[0] = 1
        elif airline == 'GoAir':
            airlines_row[1] = 1
        elif airline == 'IndiGo':
            airlines_row[2] = 1
        elif airline == 'Jet Airways':
            airlines_row[3] = 1
        elif airline == 'Jet Airways Business':
            airlines_row[4] = 1
        elif airline == 'Multiple carriers':
            airlines_row[5] = 1
        elif airline == 'Multiple carriers Premium economy':
            airlines_row[6] = 1
        elif airline == 'SpiceJet':
            airlines_row[7] = 1
        elif airline == 'Trujet':
            airlines_row[8] = 1
        elif airline == 'Vistara':
            airlines_row[9] = 1
        elif airline == 'Vistara Premium economy':
            airlines_row[10] = 1

        Source = request.form["Source"]
        sources_row = np.zeros(4, dtype=int)
        if Source == 'Chennai':
            sources_row[0] = 1
        elif Source == 'Delhi':
            sources_row[1] = 1
        elif Source == 'Kolkata':
            sources_row[2] = 1
        elif Source == 'Mumbai':
            sources_row[3] = 1

        Dest = request.form["Destination"]
        dest_row = np.zeros(5, dtype=int)
        if Dest == 'Cochin':
            dest_row[0] = 1
        elif Dest == 'Delhi':
            dest_row[1] = 1
        elif Dest == 'Hyderabad':
            dest_row[2] = 1
        elif Dest == 'Kolkata':
            dest_row[3] = 1
        elif Dest == 'New Delhi':
            dest_row[4] = 1

        add_info = request.form['add_info']
        add_info_row = np.zeros(9, dtype=int)
        if add_info == '1 Short layover':
            add_info_row[0] = 1
        elif add_info == '2 Long layover':
            add_info_row[1] = 1
        elif add_info == 'Business class':
            add_info_row[2] = 1
        elif add_info == 'Change airports':
            add_info_row[3] = 1
        elif add_info == 'In-flight meal not included':
            add_info_row[4] = 1
        elif add_info == 'No Info':
            add_info_row[5] = 1
        elif add_info == 'No check-in baggage included':
            add_info_row[6] = 1
        elif add_info == 'No info':
            add_info_row[7] = 1
        elif add_info == 'Red-eye flight':
            add_info_row[8] = 1

        inp = np.append([Total_stops, Journey_day, Journey_month, Journey_weekday, Dep_hour, Dep_min, Arrival_hour, Arrival_min, dur_hour, dur_min], airlines_row)
        inp = np.append(inp, sources_row)
        inp = np.append(inp, dest_row)
        inp = np.append(inp, add_info_row)

        prediction=model.predict([inp])

        output=round(prediction[0],2)

        return render_template('index.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)
