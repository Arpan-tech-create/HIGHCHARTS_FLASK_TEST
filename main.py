from flask import Flask, render_template, jsonify,request
from pytz import timezone
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file using pandas
    data = pd.read_csv('data.csv')

    # Convert the timestamp column to datetime format
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], format='%d/%b/%Y:%H:%M:%S:%z')

    # Extract the date and hour from the timestamp
    data['Date'] = data['TIMESTAMP'].dt.date
    data['Hour'] = data['TIMESTAMP'].dt.strftime('%H')

    # Count the occurrences of each date
    date_counts = data['Date'].value_counts().sort_index()

    # Prepare the original data for Highcharts
    original_data = [{'name': str(date), 'y': count} for date, count in date_counts.items()]

    # Group the data by date and hour, and calculate the hourly counts
    hourly_data = data.groupby(['Date', 'Hour']).size().reset_index(name='Count')

    # Prepare the hourly data for Highcharts
    hourly_data_dict = {}
    for _, row in hourly_data.iterrows():
        date = str(row['Date'])
        hour = row['Hour']
        count = row['Count']
        if date not in hourly_data_dict:
            hourly_data_dict[date] = []
        hourly_data_dict[date].append([hour, count])

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

    # Pass the original data, hourly data, and pie data to the template
    return render_template('chart.html', original_data=original_data, hourly_data=hourly_data_dict, pie_data=pie_data, from_date=from_date, to_date=to_date)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
