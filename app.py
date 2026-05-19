from flask import Flask
from models import db
from flask import render_template,request
from models import Student
from flask import redirect, url_for
from models import PlacementDrive
from models import Application
from flask import session
from models import Company
app=Flask(__name__)
app.secret_key="secret123"


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)



@app.route("/student/register",methods=["GET","POST"])

def student_register():

    if request.method== "POST":

        name= request.form["name"]
        email = request.form["email"]
        password= request.form["password"]
        resume= request.form["resume"]

        new_student = Student(
            name=name,
            email=email,
            password=password,
            resume=resume
        )

        db.session.add(new_student)
        #db.session.commit()
        db.session.commit()
        return redirect('/login_student')  

        # After register → go to login
        

    #  For GET-show registration form
    return render_template("student_register.html")



from models import Company
@app.route("/company/register", methods=["GET","POST"])

def company_register():

    if request.method== "POST":

        company_name = request.form["company_name"]
        hr_contact = request.form["hr_contact"]
        website = request.form["website"]

        new_company = Company(
            company_name=company_name,
            hr_contact=hr_contact,
            website=website
        )

        db.session.add(new_company)
        db.session.commit()

        #return "Company Registered Successfully (Waiting for Admin Approval)"
        return render_template("company_success.html")

    return render_template("company_register.html")    



@app.route("/admin/companies")
def view_companies():

    companies = Company.query.all()

    return render_template("admin_companies.html", companies=companies)





@app.route("/admin/approve/<int:company_id>")
def approve_company(company_id):

    company = Company.query.get(company_id)

    company.approval_status = "Approved"

    db.session.commit()

    return redirect(url_for("view_companies"))





@app.route("/company/create_drive", methods=["GET","POST"])
def create_drive():

    if request.method == "POST":

        job_title = request.form["job_title"]
        description = request.form["description"]
        eligibility = request.form["eligibility"]
        deadline = request.form["deadline"]
        company_id = session['company_id']

        new_drive = PlacementDrive(
            job_title=job_title,
            description=description,
            eligibility=eligibility,
            deadline=deadline,
            company_id=company_id
        )

        db.session.add(new_drive)
        db.session.commit()

        return "Placement Drive Created Successfully"

    return render_template("create_drive.html")





@app.route("/drives")
def view_drives():

    drives = PlacementDrive.query.all()

    return render_template("drives.html", drives=drives)




@app.route("/apply/<int:drive_id>")
def apply_drive(drive_id):

    if 'student_id' not in session:
        return redirect('/login_student')

    student_id = session['student_id']

    existing = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing:
        return "You have already applied for this drive"

    new_application = Application(
        student_id=student_id,
        drive_id=drive_id
    )

    db.session.add(new_application)
    db.session.commit()

    return redirect('/student/dashboard')



@app.route("/applications")
def view_applications():

    applications = Application.query.all()

    return render_template("applications.html", applications=applications)




@app.route("/application/update/<int:app_id>/<status>")
def update_application(app_id, status):

    application = Application.query.get(app_id)

    application.status = status

    db.session.commit()

    return redirect(url_for("view_applications"))



@app.route("/student/dashboard")
def student_dashboard():

    if 'student_id' not in session:
        return redirect('/login_student')

    student_id = session['student_id']

    # get applications of this student
    applications = Application.query.filter_by(student_id=student_id).all()

    # get student details
    #student = Student.query.get(student_id)
    student = db.session.get(Student, student_id)

    #  RETURN must be inside function
    return render_template(
        "student_dashboard.html",
        applications=applications,
        student=student
    )


@app.route("/admin/dashboard")
def admin_dashboard():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    return render_template(
        "admin_dashboard.html",
        students=total_students,
        companies=total_companies,
        drives=total_drives,
        applications=total_applications
    )


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin/students")
def view_students():
    students = Student.query.all()
    return render_template("admin_students.html", students=students)    


#from models import Company

@app.route('/login_student', methods=["GET","POST"])
def login_student():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        #STUDENT LOGIN
        if role == "student":
            student = Student.query.filter_by(email=email, password=password).first()

            if student:
                session['student_id'] = student.id
                return redirect('/student/dashboard')

        # COMPANY LOGIN
        elif role == "company":
            company = Company.query.filter_by(hr_contact=email).first()

            if company:
                session['company_id'] = company.id
                return redirect('/company/create_drive')

        return "Invalid credentials"

    return render_template("login.html")

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)