from flask import Flask, render_template, jsonify
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
    data['Hour'] = data['TIMESTAMP'].dt.strftime('%H:%M:%S')

    # Count the occurrences of each date
    date_counts = data['Date'].value_counts().sort_index()

    # Prepare the original data for Highcharts
    original_data = [{'name': str(date), 'y': count} for date, count in date_counts.items()]

    # Pass the original data to the template
    return render_template('chart.html', original_data=original_data, hourly_data=data.to_dict('records'))

if __name__ == '__main__':
    app.run()
