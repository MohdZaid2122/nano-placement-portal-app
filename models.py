from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    resume = db.Column(db.String(200))
    

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(100))
    password = db.Column(db.String(100))
    approval_status = db.Column(db.String(20), default="Pending")


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    eligibility = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    status = db.Column(db.String(20), default="Pending")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))
    status = db.Column(db.String(20), default="Applied")
    
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    resume = db.Column(db.String(200))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(100))
    approval_status = db.Column(db.String(20), default="Pending")

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    eligibility = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    status = db.Column(db.String(20), default="Pending")
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))
    status = db.Column(db.String(20), default="Applied")
