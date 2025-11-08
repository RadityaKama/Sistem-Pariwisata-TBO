from flask import Flask, render_template, request, redirect, url_for, flash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_csv(file_name):
    data = []
    try:
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

def save_csv(file_name, fieldnames, data):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    file_name = 'users.csv'
    fieldnames = ['username', 'password']
    users = load_csv(file_name)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if any(user['username'] == username for user in users):
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        new_user = {'username': username, 'password': password}
        users.append(new_user)
        save_csv(file_name, fieldnames, users)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    file_name = 'users.csv'
    users = load_csv(file_name)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if any(user['username'] == username and user['password'] == password for user in users):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/places', methods=['GET', 'POST'])
def places():
    file_name = 'place_activity.csv'
    fieldnames = ['id', 'name', 'description']
    places = load_csv(file_name)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_place = {'id': str(len(places) + 1), 'name': name, 'description': description}
        places.append(new_place)
        save_csv(file_name, fieldnames, places)
        flash('Place added successfully!', 'success')
        return redirect(url_for('places'))

    return render_template('places.html', places=places)

@app.route('/events', methods=['GET', 'POST'])
def events():
    file_name = 'event_activity.csv'
    fieldnames = ['id', 'name', 'date']
    events = load_csv(file_name)

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        new_event = {'id': str(len(events) + 1), 'name': name, 'date': date}
        events.append(new_event)
        save_csv(file_name, fieldnames, events)
        flash('Event added successfully!', 'success')
        return redirect(url_for('events'))

    return render_template('events.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
