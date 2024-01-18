from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

# create the Flask application
app = Flask(__name__)

# create the SQLAlchemy database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create the database model
class Bio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.Text)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    resume = db.Column(db.Text)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

# create the database tables
db.create_all()

# create the routes for the application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bio', methods=['GET', 'POST'])
def bio():
    if request.method == 'POST':
        bio = Bio(name=request.form['name'], bio=request.form['bio'])
        db.session.add(bio)
        db.session.commit()
        return redirect(url_for('index'))
    bios = Bio.query.all()
    return render_template('bio.html', bios=bios)

@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        resume = Resume(name=request.form['name'], resume=request.form['resume'])
        db.session.add(resume)
        db.session.commit()
        return redirect(url_for('index'))
    resumes = Resume.query.all()
    return render_template('resume.html', resumes=resumes)

@app.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        project = Project(name=request.form['name'], description=request.form['description'])
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))
    projects = Project.query.all()
    return render_template('project.html', projects=projects)

if __name__ == '__main__':
    # run the Flask application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)