from os import error
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
import re

app = Flask(__name__) 

tasks = [ #list of dictionaries containing required info abt each task

    {
        'task' : 'get milk', 
        'assigned' : 'connor@mail.com', 
        'priority' : 'low'
    },
    {
        'task' : 'cook dinner', 
        'assigned' : 'peggy@mail.com', 
        'priority' : 'high'
    },
    {
        'task' : 'do dishes', 
        'assigned' : 'monk@mail.com', 
        'priority' : 'medium'
    }
]

@app.route('/') 
def display_list():
    return render_template('index.html', tasks=tasks)


@app.route('/error/<error>')
def error_message(error):
    return render_template('error.html', error=error)


@app.route('/clear', methods=['POST'])
def clear_table():
    tasks.clear()
    return redirect('/')
    

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
        #     return "Please enter valid priority level" #these errors can be same page just change variable
            error = 'priority'
    else:
        # return "Please enter a valid email address" #change to an error page w return button
        error = 'email'
        return redirect(url_for('error_message', error=error))
        

if __name__ == '__main__': 
    app.run(debug=True)
