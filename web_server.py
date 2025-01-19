"""
Author: Abhishek Dhiman
Email: sigmasix09@gmail.com
"""

from flask import Flask, render_template, request, redirect
import csv
import time

# For receiving messaging
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# For messaging to owner.
from twilio.base.exceptions import TwilioRestException

# importing security headers
from flask_talisman import Talisman
from flask_cors import CORS

# instantiating flask app instance setting name as main
app = Flask(__name__)
print(__name__)

# implementing security headers
Talisman(app, frame_options='DENY', content_security_policy={})
CORS(app, resources={r'*': {'origins': "http://sigmasix09.pythonanywhere.com/"}}, methods=['GET', 'POST'])

'''
Step 1
    0. Use python 3.10.11 for integrity of all python packages
    1. Use command prompt to clone the git repository to required directory
    2. git clone <repo url>
    3. open the IDE (pycharm) and open the directory as project
    4. Setup the python interpreter
    5. Install the packages using terminal: pip install -r requirements.txt
    
    0. Create virtual env as per the local python version but could harm python packages used
    1. creating virtual environment: python -m venv venv or use VScode/IDE settings 
    2. activate venv: venv\Scripts\activate.bat
    3. Change (Pycharm): Tools > terminal > shell path > cmd.exe
    3. Read more: https://python.land/virtual-environments/virtualenv


Step 2: Important git commands
    1. To see all branches: git branch -a
    2. Delete local branch: git branch -d branch-name
    3. Delete remote branch: git push origin -d branch-name
    4. Pull changes from remote: git pull origin
    5. Check the status of current branch: git status
    6. Add changes to commit: git add .
    7. Commit or save changes to branch: git commit -m'commit_message'
    8. Push the changes to remote or local: git push origin master or git push

Step 3: Running local host server
    1. Environment variable for ENV: set FLASK_ENV=development
    2. Environment variable for APP: set FLASK_APP=web_server.py
    3. Command to run the flask app: flask run

Step 4: Cleaning temp files on pythonanywhere.com
    1. Bash command: rm -rf /tmp/* /tmp/.*
    2. Bash command: rm -rf ~/.cache/*

'''

'''
##### web_server.py file information #####

This script is for web development purpose.
It works on 3 basic files: html(text on te web page), CSS(styling), JS(behaviour/actions)
When browser make request, the server send the 3 files to it and display the request web page.
The server can be coded using python.
html, css, js files received from server is of type document, css and js respectively.
Building Server using 'FLASK' framework
render_template: allows user to send the html file
template folder: to store only html files.
static folder: to store css adn js file
favicon: {{ python expression }} is jinja templating
'''

# 1st file's decorators
'''
@app.route('/<username>/<int:age>')
def hello_world(username=None, age=None):
    return render_template('text.html', name=username, age=age)


@app.route('/details/<username>/<int:age>')
def my_details(username=None, age=None):
    return render_template('details.html', name=username, age=age)
'''


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def web_name(page_name):
    return render_template(page_name)


@app.route('/contact_form', methods=['POST', 'GET'])
def contact_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        send_data_to_owner(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong, please try again later.'


'''
This function writes the details of contact form into a csv file.
Add a new line in the csv file.
Github account: ateamas; for storing these files.
PythonAnywhere: sigmasix; for creating the website.
Setting up: https://help.pythonanywhere.com/pages/Flask/
Website: http://sigmasix09.pythonanywhere.com/index.html
Projects: 8 project have been mentioned
'''


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as f1:
        email = data["Email"]
        subject = data["Subject"]
        message = data["Message"]
        csv_writer = csv.writer(f1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([time.asctime(time.localtime()), email, subject, message])


def send_data_to_owner(data):
    """
    This function takes the visitor's entered data and send
    an SMS to the owner with the data.
    """

    message_item = [time.asctime(time.localtime()), data["Email"], data["Subject"], data["Message"]]
    try:
        import config
        account_sid = config.AppConfig.ACCOUNT_SID.replace("--", "")
        auth_token = config.AppConfig.AUTH_TOKEN.replace("--", "")
        proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ[
            'https_proxy']})
        client = Client(account_sid, auth_token, http_client=proxy_client)
        message = client.messages.create(
            from_=config.AppConfig.sender_num,
            body=str(message_item),
            to=config.AppConfig.receiver_num
        )
        print(message.sid)
        print("Executed Successfully.")
    except TwilioRestException as e:
        print(e)
