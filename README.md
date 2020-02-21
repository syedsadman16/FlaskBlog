# Flask Blog

Simple blog created using Python Flask framework and Html/Css



Preview             
:-------------------------:
<img src='demo.gif' title='Demo' width='' alt='Demo' /> 



## Notes
Personal notes taken while working on project

- Need to convert template to use jinja and flask
- Create routes for each html page. 
- SQLAlehemy: Install using pip >> sqlite3 [name].db >> .tables to save the database
- Create a table to hold information about each post >> Models

#### Basics
- View functions handle application routes to different URLs. There are decorators (@app.route) which load a URL to a web page and execute functions and logic defined. 
```Python
 @app.route('/index')
 def index():
     return "Hello, World!"
```
- Templates help create seperation between design and logic. Template folder contains HTML. 
- Static folder is where JavaScript and CSS are stored
```python
 '{{ url_for('static', filename='file.css') }}'
```
- Variables for dynamic content represented by {{ ... }} which is only known at runtime. 
- To set value of variables, define it when the template is rendered as parameters of the render_template method. 
```python
 <title>{{ title }} - Microblog</title>
 <h1>Hello, {{ user.username }}!</h1>
```
```python
 @app.route('/index')
 def index():
     user = {'username': 'Miguel'}
     return render_template('index.html', title='Home', user=user)
```

***

#### Conditionals
If/Else loops
```python
  {% if title %}
      <title>{{ title }} - Microblog</title>
  {% else %}
      <title>Welcome to Microblog!</title>
  {% endif %}
```

For loops 
- Define users posts as a list inside function
```python
 posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        ....
    ]
```
- It will take each list object and populate all fields.
```python
 {% for post in posts %}
     <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
 {% endfor %}
```

***


#### Input from Forms
Define form with method and route 

```python
 <form method="POST" action="{{ url_for('submit') }}" class="...">
```
Handle form data in route

```python
@app.route('/submit', methods=['POST'])
def submit():
```



#### Setting up a database
Flask gives freedom in choosing database. Using SQLAlchemy since its a conventient choice to run quickly on desktop instead of an online server

- install database with pip and import it into project
- set up the database location
- initiate the database in terminal

In directory where app is installed
```bash
sqlite3 [database_name].db
.tables // To save the database
.exit
```

```bash
from app import db
db.create_all()
exit()
```


- Create a class to hold the infromation and save to database - usuually called Database models
```python
class ClassName(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30))
  name = db.COlumn(db.Text)
  .... 
```


***

#### Saving data to database
Once database is setup, now create a way for the database content to be saved and displayed. 

- Database information is stored using a form. The page with the form should already hava a route with its template rendered.
- When the form is being sumbitted, that needs another route. Import request into flask. Now create the function and specify the method. By default its GET so make this POST since uploading data. 

```python
@app.route('/submit', methods=['POST'])
def submit():
  title = request.form['title']
  name = request.form['name']

  post = Classname(title=title, name=name)
  db.session.add(post)
  db.session.commit()
  return redirect(url_for('index'))
  ```
- Add fields to database and redirect to go to some page

- Can also use this jsut to check what was entered 
```Python
    return "'<h1>Title: {} Name: {} </h1>'".format(title, name) 
```
- Or in terminal
```bash
    sqlite database.db
    .tables
    select * from [table_name]
```
- This basically takes input from the form based on an id value and assigns it to a variable. Then it returns 

- Next, the App needs to know which form to call the function on. So specify it as seen below:
```Python
  <form name="addForm" id="addForm" method="POST" action="{{ url_for('submit') }}" novalidate>
```

***

#### Retrieving single database entry
Once everythign is saved, the data should be displayed. 

- First update app.py routes. Since there is a primary key set to identify each post, query the database for that post id. 
```python
@app.route('/display/<int:post_id>')
def display(post_id):
  post = Blogpost.query.filter_by(id=post_id).one()
reutrn render_template('viewposts.html', post=post)
```
- Route is updated, now specify in html where it should be uploaded. This can be referenced anywhere in the page, doesnt have to be bound under one div only. 

viewposts.html
```python
<div>
  <h1> {{ post.title }} </h1>
  <h1> My name is {{ post.name }} </h1>
  ....
  {{ post.content|safe }} 
```
- Safe keyword prevents < > tags from being shown and formats it correctly. Also prevents others from typing in html and loading it. 

***

#### Displaying all data 
Since a single post can be displayed on one page, what about multiple posts from the database? Change rouute and pass all data to the template

```python
@app.route('/')
def index():
  posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
  return render_template('index.html', posts=posts)
```
- Now set up a loop inside the html
```python
<div class=container>
  {% for post in posts %}
    ....
    {{ post.title }} 
  {% endfor %}
</div>
```

- Each post is referenced by its post id. Can be passed to a new route with given parameters which is handled in app.py
```python
<div class=container>
  <a href={{url_for('route_name', post_id = post.id)}}
</div>
```


## Resources Used

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/


