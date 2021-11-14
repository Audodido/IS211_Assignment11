from os import error
from flask import Flask, render_template, request, url_for, redirect
from os.path import exists
import re


app = Flask(__name__) 

tasks = [] #list of dictionaries containing required info abt each task

@app.route('/') 
def display_list():
    return render_template('index.html', tasks=tasks)


@app.route('/error/<error>')
def error_message(error):
    return render_template('error.html', error=error)


@app.route('/save', methods=['POST'])
def save_list():
    with open('list_archive.txt', 'w+', encoding='utf-8') as f:
        for t in tasks:
            f.writelines(f"{t['task']}, {t['assigned']}, {t['priority']}\n")
    return redirect('/')


@app.route('/clear', methods=['POST'])
def clear_table():
    tasks.clear()
    return redirect('/')
    
    
## Extra credit II
# @app.route('/delete', methods=['POST'])
# def delete_row():
#     to_go = request.form['']
#     tasks.append({'to go' : to_go})


@app.route('/submit', methods=['POST'])
def submit():
    new_task = request.form['task']
    new_assigned = request.form['assigned to']
    new_priority = request.form['priority']

    if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', new_assigned):
        if re.match(r'low|medium|high', new_priority, re.IGNORECASE):
            tasks.append({
                'task' : new_task,
                'assigned' : new_assigned,
                'priority' : new_priority})
            # return tasks[len(tasks)-1]
            # return render_template('post.html')
            return redirect('/')
        else:
            error = 'priority'
    else:
        error = 'email'
        return redirect(url_for('error_message', error=error))
        

if __name__ == '__main__':

    if exists('list_archive.txt'):
        with open ('list_archive.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                for line in lines:
                    entry = line.split(',')
                    tasks.append({
                        'task' : entry[0],
                        'assigned' : entry[1],
                        'priority' : entry[2]})
                

        app.run(debug=False)
