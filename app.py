from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
df = pd.read_excel('./data/planner.xlsx')

# Dictionary to store changes
changes = {}

@app.route('/')
def display_table():
    return render_template('index.html', table=df.to_html(classes='data'), title='Таблица Excel')

@app.route('/edit', methods=['POST'])
def edit():
    row = int(request.json['row'])
    col = int(request.json['col'])
    new_value = request.json['value']

    # Save changes to the dictionary
    changes[(row, col)] = new_value
    print('edit')

    return jsonify({'status': 'success'})

@app.route('/save_changes', methods=['POST'])
def save_changes():
    # new_value = {}
    new_value=request.json
    
    print(new_value)
    print('________________')
    global df
    # Apply changes to the DataFrame
    for (row, col), value in changes.items():
        df.iat[row, col-1] = value

    # Save changes to the Excel file
    df.to_excel('./data/planner.xlsx', index=False)
    
    # Clear the changes dictionary
    changes.clear()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run()
