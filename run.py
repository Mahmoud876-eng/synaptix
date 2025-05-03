import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request , session, redirect, jsonify
from flask_session import Session
import pyttsx3


app = Flask(__name__)
#sert secret key for session management
app.config["SECRET_KEY"] = "your_secret_key_here"
#session 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session = Session(app)

#from flask_session import Session

# Load your service account key
cred = credentials.Certificate("firebase_mahmoud.json")

# Initialize the app (only once!)
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# creating the data bases
student_collection = db.collection('student')
teacher_collection=db.collection('teacher')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST","GET"] )#connect the test1.py and the flask here got an error when u click the button in the middle
def register():
    
    if request.method == "POST":
        print("nice")
        email= request.form.get("email") 
        password=request.form.get("password")
        
        username=request.form.get("username")
        niveau=request.form.get("niveau")
        teacher=request.form.get("teacher")
        
        print(email)
        print("k")
        student_with_teacher = list(teacher_collection.where('username', '==', teacher).stream())
        if not student_with_teacher:
            return render_template("error.html",message="teacher not found")
        student_with_mail = list(student_collection.where('email', '==', email).stream())
        teacher_with_mail = list(teacher_collection.where('email', '==', email).stream())
        print(student_with_mail)
        if student_with_mail or teacher_with_mail:
            return render_template("error.html",message="mail already exist")
        
        if len(password) < 8:
            return render_template("error.html",message="password too short")
    
        
        print('cool')
        user_data = {
            "username": username,
            "email": email,
            "status":  "student",
            "niveau": niveau,
            "teacher": teacher,
            "password": password
        }
        
            
        inserted_user = student_collection.add(user_data)
        session["username"] = username
        #session["status"] = status
        #            
        return render_template("home_students.html")
    return render_template("register.html")
@app.route("/register/professor", methods=["POST","GET"])
def regpro():
    print("enter")
    if request.method == "POST":
        print("right")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        teacher_with_mail = list(teacher_collection.where('email', '==', email).stream())
        if  teacher_with_mail:
            return render_template("error.html",message="mail already exist")
        if len(password) < 8:
            return render_template("error.html",message="password must be at least 8 characters")
        user_data = {
            "username": username,
            "email": email,
            "status":  "Teacher",
            "password": password
            }
        
            
        inserted_user = teacher_collection.add(user_data)
        session["username"] = username
        return render_template("professor_dashboard.html",username=username)
    return render_template("register_p.html")



@app.route("/login", methods=["POST","GET"] )
def login_student():
    print(request.method)
    if request.method == "POST":
        #get the data from json 
        email = request.form.get("email")
        password = request.form.get("password")
        print(email)

        if not password or not email:
            return render_template("error.html", message="missing password")
        
        student_with_mail = list(student_collection.where('email', '==', email).stream())
        teacher_with_mail = list(teacher_collection.where('email', '==', email).stream())
        print(teacher_with_mail)
        print(student_with_mail)
        
        
        if student_with_mail:    
            print("5")
            student_data = student_with_mail[0].to_dict()
            print("69")
            if student_data['password'] != password:  # In real apps, use hashed passwords!
                print("no")
                
                return render_template("error.html",message="wrong password")    
            print("55")        
            #session["user_id"] = user_with_mail['_id']
            #session["status"] = user_with_mail['status']
            #session["username"] = user_with_mail['username']
            #return jsonify({"status": "user","username": user_with_mail['username']}), 200                # return render_template("home_usr.html",username=user_with_mail['username'])
            return render_template("home_students.html")
        elif teacher_with_mail:
            teacher_data = teacher_with_mail[0].to_dict()
            if teacher_data['password'] != password:  # In real apps, use hashed passwords!

                return render_template("error.html",message="wrong password") 
            print('77')
            pro_data = teacher_with_mail[0].to_dict()
            user_name = pro_data['username']
            #session["user_id"] = doctor_with_mail['_id']
            #session["status"] = doctor_with_mail['status']
            print(user_name)
            session["username"]=user_name
            #return jsonify({"status": "doctor","username": doctor_with_mail['username']}), 200
            #return render_template("home_doctor.html",username=doctor_with_mail['username'])
            return render_template("professor_dashboard.html")
        else:
            return render_template("error.html", message="mail not found")     
    return render_template("login.html")


@app.route("/professor", methods=["post","GET"])
def professor():
    teacher= session.get('username')
    teacher_with_mail = list(student_collection.where('teacher', '==', teacher).stream())
    all_teachers = list(student_collection.stream())
    
    # Convert to list of dictionaries
    data = [doc.to_dict() for doc in teacher_with_mail]
    print(data)
    return render_template("test.html",students=data,name=teacher)
def speak_message(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Configure voice properties (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female (varies by system)
    engine.setProperty('rate', 100)  # Speed of speech (words per minute)
    
    # Speak the message
    engine.say(text)
    engine.runAndWait()
@app.route("/talk", methods=["POST","GET"])
def talk():
    print("66")
    if request.method == "POST":
        print("55")
        message = request.form.get("userText")
        print(message)

        # Speak the message
        speak_message(message)
        print(f"Speaking: '{message}'")
    return render_template("talk.html")
@app.route("/home_student")
def home_student():
    return render_template("home_students.html")
@app.route("/marqet")
def marqet():
    return render_template("marqet.html")
@app.route("/maquette")
def maquette():
    return render_template("maquette.html")
@app.route("/card")
def card():
    return render_template("card.html")
@app.route("/flyer")
def flyer():
    return render_template("flyer.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)