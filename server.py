from flask import Flask, render_template, url_for, request
import csv

from jinja2.lexer import newline_re

app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(f"{page_name}.html")

# @app.route('/test')
# def test_route():
#     return render_template('password-checker.html')

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f"Email: {email}\nSubject: {subject}\nMessage: {message}\n{'-' * 40}\n")

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            write_to_csv(data)
            return 'form submitted'
        except:
            print('data not written to db')
    else:
        return 'something went wrong'