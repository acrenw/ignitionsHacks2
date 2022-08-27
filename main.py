import random, string
from flask import Flask, render_template, request
import requests, json
# from werkzeug import secure_filename

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits


@app.route('/')  # What happens when the user visits the site
def base_page():
	url = "https://api.symbl.ai/oauth2/token:generate"
	
	payload = {
	    "type": "application",
	    "appId": "4841486a5565723339476c556a396639453855365342344b30486a694d336972",
	    "appSecret": "6a2d624c78736538466135394467323345647633545966314e784d44344e35427133456a426565462d5f4a494b6b7135676563724463624d336d776d2d454d49"
	}
	headers = {
	    "Accept": "application/json",
	    "Content-Type": "application/json"
	}
	
	response = requests.post(url, json=payload, headers=headers)
	
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
		accessToken = response.json()['accessToken']  # Sets the variable random_number in the template
	)


@app.route('/2')
def page_2():
	rand_ammnt = random.randint(10, 100)
	random_str = ''.join(random.choice(ok_chars) for a in range(rand_ammnt))
	return render_template('site_2.html', random_str=random_str)


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
		debug=True
	)