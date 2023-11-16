from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_excel('./data/planner.xlsx')

changes = {}

df.index = df.index + 1

@app.route('/')
def display_table():
    
    return render_template('index.html', table=df.to_html(classes='data'), title='Главная таблица')

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
    global df
    # сохраним df в качестве предыдущей версии
    excel_file_path = './data/prev_planner.xlsx'
    df.to_excel(excel_file_path, index=False)

    new_value=request.json
    changes = new_value['arr']

    print('________________')
   
    # Apply changes to the DataFrame
    for  value in changes:
        df.iat[value['row'], value['col']-1] = value['newContent']
        
    print(df)
    # Save changes to the Excel file
    df.to_excel('./data/planner.xlsx', index=False)
    
    # Clear the changes dictionary
    changes.clear()

    return jsonify({'status': 'success'})


@app.route('/prev_planner', methods=['GET'])
def prev_planner():
    global prev_df
    prev_df = pd.read_excel('./data/prev_planner.xlsx')
    print(prev_df)
    print(df)
    prev_df.index = prev_df.index + 1
    return render_template('index.html', table=prev_df.to_html(classes='data'), title='Предыдущая таблица')


@app.route('/rollback_planner', methods=['POST'])
def rollback_planner(): 
    global prev_df
    global df
    df = prev_df
    df = pd.read_excel('./data/prev_planner.xlsx')

    excel_file_path = './data/planner.xlsx'
    df.to_excel(excel_file_path, index=False)
    return render_template('index.html', table=df.to_html(classes='data'), title='Предыдущая таблица')


if __name__ == '__main__':
    app.run()
