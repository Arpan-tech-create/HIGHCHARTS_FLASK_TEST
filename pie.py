from flask import Flask, render_template, request
import pandas as pd
from pytz import timezone

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file using pandas
    data = pd.read_csv('data.csv')

    # Convert the timestamp column to datetime format
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], format='%d/%b/%Y:%H:%M:%S:%z')

    # Filter the data based on the date range provided in the query parameters
    from_date = request.args.get('from-date')
    to_date = request.args.get('to-date')

    if from_date and to_date:
        from_date = pd.to_datetime(from_date).tz_localize(timezone('UTC'))
        to_date = pd.to_datetime(to_date).tz_localize(timezone('UTC'))
        filtered_data = data[(data['TIMESTAMP'] >= from_date) & (data['TIMESTAMP'] <= to_date)]
    else:
        filtered_data = data

    # Filter the data for RESPONSE 403
    filtered_data = filtered_data[filtered_data['RESPONSE'] == 403]

    # Count the occurrences of each message
    message_counts = filtered_data['MESSAGE'].value_counts()

    # Prepare the data for the pie chart
    pie_data = [{'name': message, 'y': count} for message, count in message_counts.items()]

    # Pass the pie data and date range to the template
    return render_template('pie.html', pie_data=pie_data, from_date=from_date, to_date=to_date)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
