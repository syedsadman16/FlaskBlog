from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# location for the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


# Create a database model to be pushed to database
class BlogEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	author = db.Column(db.String(25))
	content = db.Column(db.Text)
	date = db.Column(db.DateTime)



# routes to render pages
@app.route('/')
def index():
	posts = BlogEntry.query.order_by(BlogEntry.date.desc()).all()

	return render_template("index.html", posts=posts)


@app.route('/create')
def create():
    return render_template("create_post.html")


# Route user to post clicked on from index
@app.route('/view/<int:post_id>')
def view(post_id):
    post = BlogEntry.query.filter_by(id=post_id).one()
    return render_template('view_post.html', post=post)


# route to retrieve data and upload to database
@app.route('/submit', methods=['POST'])
def submit():
	title = request.form['title']
	author = request.form['author']
	content = request.form['content']

	post = BlogEntry(title=title, author=author, content=content, date=datetime.now())

	db.session.add(post)
	db.session.commit()

	return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

