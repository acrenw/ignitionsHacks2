So I saw that there was no (complete) flask tutorials here, so I'm going to start this series.
***
Now before we start, its assumed that you already know basic html, so if you don't know html I recommend that you learn it first.  This part is only the basics of flask, its not intended for advanced users.

## Step 1: Install flask
Now first of all, you need to add the package flask to your repl. To do so, use the repl package manager. If you are for some reason, not using repl, simply run `sudo pip3 install flask` (assuming you already have python installed).
To install flask on repl, open the package manager:
![Open package manager](https://i.ibb.co/j6PRmJS/Screenshot-2020-01-18-Flask-Tutorial-1.png "Open package manager")
Then search for flask
![Search for flask](https://i.ibb.co/VYSyqPc/Screenshot-2020-01-18-Flask-Tutorial-1-1.png "Search for flask")
Finaly, click on Flask and hit the +
![Install flask](https://i.ibb.co/YX5L1pz/Screenshot-2020-01-18-Flask-Tutorial-1-2.png "Install Flask")
You should then see flask install.
***
## Step 2: Setup
This is to initialize your flask app, without any web pages.

So to start off, you will need your app object, so you can get that with:
```python
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)
```
Then, to start the app:
```python
if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
```
Now, once you run this, you should get a page saying "Not Found" or a 404 error
***
## Step 3: Making your first page
So to add a page to your site, simply add `@app.route('/(page-path)')` and on the next line, a function that doesnt take any arguments. To return an output, you can either return a string, or make a more advanced output.
A basic output:
```python
@app.route('/')  # '/' for the default page
def home():
	return "Wow this is a basic output!"
```
But you can also render an html file/template:
```python
def base_page():
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
	)
```
In base.html:
```html
<h1>Hello there!</h1>
```

Now, when you run the page it should say "Hello there!"

***
## Step 4: Use variables
Now, it gets a bit more fun. What we are doing now, is adding variables to be used in the template.
To add a variable to be used by the template simply add `var_name=variable` and the template will be able to read `variable` by using `{{ var_name }}`
```python
@app.route('/')  # What happens when the user visits the site
def base_page():
	random_num = random.randint(1, 100000)  # Sets the random number
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
		random_number=random_num  # Sets the variable random_number in the template
	)
```
In templates/base.html:
```html
<h1>The number is {{ random_number }}</h1>
```
***
## A full example:
In main.py:
```python
import random, string
from flask import Flask, render_template

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits


@app.route('/')  # What happens when the user visits the site
def base_page():
	random_num = random.randint(1, 100000)  # Sets the random number
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
		random_number=random_num  # Sets the variable random_number in the template
	)


@app.route('/2')
def page_2():
	rand_ammnt = random.randint(10, 100)
	random_str = ''.join(random.choice(ok_chars) for a in range(rand_ammnt))
	return render_template('site_2.html', random_str=random_str)


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
```

In static/base.css:
```css
cb { background-color: rgb(63, 63, 63) }

a {
	color: black;
	-webkit-appearance: button;
	-moz-appearance: button;
	appearance: button;
	
}

body {
	text-align: center;
	font-family: 'IBM Plex Sans', sans-serif;
	background-color: black;
	color: white;
}
```

In templates/base.html:
```html
<!doctype html>
<head>
	<title>Flask Tutorial!</title>
	<script src="/static/base.js"></script>
	<link href="/static/base.css" rel="stylesheet" type="text/css">
	<link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans&display=swap" rel="stylesheet"> 
</head>
<body>
	<h1>Hello!</h1>
	<p>
		The random number is:
		<cb>{{ random_number }}</cb>! <!--Gets the random number from the python file-->
	</p>
	<a href="/2">Visit site 2</a>
</body>
```

In templates/site_2.html:
```html
<!doctype html>
<head>
	<title>Flask Tutorial!</title>
	<script src="/static/base.js"></script>
	<link href="/static/base.css" rel="stylesheet" type="text/css">
	<link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans&display=swap" rel="stylesheet"> 
</head>
<body>
	<h1>Hello!</h1>
	<p>
		The random string is:
		<cb>{{ random_str }}</cb>! <!--Gets the random number from the python file-->
	</p>

	<a href="/">Go back</a>
</body>
```
![Base page](https://i.ibb.co/MGW2XMM/Screenshot-2020-01-18-Flask-Tutorial.png "Home page")
![Page at /2](https://i.ibb.co/71zzvwr/Screenshot-2020-01-18-Flask-Tutorial-1.png "/2")

