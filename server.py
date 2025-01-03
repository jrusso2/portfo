from flask import Flask, render_template, request, jsonify, abort
import csv
import requests
import os

app = Flask(__name__)

secret_key = os.getenv('RECAPTCHA_SECRET_KEY')

@app.route('/')
def my_home():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/<string:page_name>')
def html_page(page_name):
    try:
        return render_template(f"{page_name}.html")
    except:
        abort(404)


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
            return 'something went wrong', 500
    else:
        return 'Invalid request method', 400


@app.route('/verify_recaptcha', methods=['POST'])
def verify_recaptcha():
    try:
        data = request.json  # Expecting JSON payload
        token = data.get('token')


        # Send the token to Google's verification API
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {'secret': secret_key, 'response': token}
        response = requests.post(verify_url, data=payload)
        result = response.json()

        # Add additional logging for debugging
        print(f"reCAPTCHA verification result: {result}")

        return jsonify({
            'success': result.get('success', False),
            'score': result.get('score', 0),
            'action': result.get('action', ''),
        }), 200
    except Exception as e:
        print(f"Error during reCAPTCHA verification: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
