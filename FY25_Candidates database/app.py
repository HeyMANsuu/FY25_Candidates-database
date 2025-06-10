

# *****************************************************************
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import pickle
import numpy as np
import pandas as pd
import os

# Load trained ML model + scaler
model_path = r"E:\final_ML\FY25_Candidates database\Models"
with open(os.path.join(model_path, 'scaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)

with open(os.path.join(model_path, 'mindset_model.pkl'), 'rb') as f:
    model_mindset = pickle.load(f)



app = Flask(__name__)

app.secret_key = 'skill_skore_99'  # Secret key for session management

# 1. configure sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. define your model 
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_no = db.Column(db.String(10))
    college_name = db.Column(db.String(200))
    college_city = db.Column(db.String(100))
    roll_no = db.Column(db.String(50))
    prefix = db.Column(db.String(10))
    name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    mobile = db.Column(db.String(15))
    alt_mobile = db.Column(db.String(15))
    primary_email = db.Column(db.String(120), unique=True)
    alt_email = db.Column(db.String(120))
    tenth_percent = db.Column(db.String(10))
    twelfth_percent = db.Column(db.String(10))
    graduation_degree = db.Column(db.String(100))
    grad_specialization = db.Column(db.String(100))
    graduation_cgpa = db.Column(db.String(10))
    year_of_graduation = db.Column(db.String(10))
    post_graduation_degree = db.Column(db.String(100))
    post_grad_specialization = db.Column(db.String(100))
    post_graduation_cgpa = db.Column(db.String(10))
    year_of_post_grad = db.Column(db.String(10))
    foreign_language = db.Column(db.String(100))
    foreign_lang_proficiency = db.Column(db.String(50))
    permanent_address = db.Column(db.String(300))
    permanent_city = db.Column(db.String(100))
    permanent_state = db.Column(db.String(100))
    permanent_pin = db.Column(db.String(10))
    skills = db.Column(db.Text)
    organization = db.Column(db.String(200))
    prior_experience = db.Column(db.Text)
    total_experience = db.Column(db.String(10))
    legal_pursuit = db.Column(db.String(100))



# Load the dataset
df = pd.read_csv(os.path.join(model_path, "..", "FY25_Candidates database.csv"))
CSV_FILE = os.path.join(model_path, "..", "FY25_Candidates database.csv")


# ------------------- LOGIN ROUTES ------------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again."

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ------------------- SKILL SEARCH FUNCTION ------------------- #
def unified_student_search(search_terms):
    df_clean = df.copy()
    df_clean['Technonlogies/Skills known'] = df_clean['Technonlogies/Skills known'].fillna('').str.lower()
    df_clean['Sports'] = df_clean['Sports'].fillna('no').str.lower()
    df_clean['ExtraCurriculum'] = df_clean['ExtraCurriculum'].fillna('no').str.lower()
    
    df_clean['Tech_points'] = df_clean['Tech_points'].fillna(0)
    df_clean['Sports_Points'] = df_clean['Sports_Points'].fillna(0)
    df_clean['ExxCur_Points'] = df_clean['ExxCur_Points'].fillna(0)
    
    terms = [term.strip().lower() for term in search_terms.split(",")]
    
    def matches_all_terms(row):
        combined_text = f"{row['Technonlogies/Skills known']} {row['Sports']} {row['ExtraCurriculum']}"
        return all(term in combined_text for term in terms)
    
    results = df_clean[df_clean.apply(matches_all_terms, axis=1)]
    
    students_list = []
    for _, student in results.iterrows():
        student_dict = {
            'Name': student['Candidate Name'],
            'CGPA': student['Graduation CGPA'],
            'Email': student['Primary Email ID (College)'],
            'Skills': student['Technonlogies/Skills known'],
            'Sports': student['Sports'],
            'Extracurriculars': student['ExtraCurriculum'],
            'Tech_points': student['Tech_points'],
            'Sports_Points': student['Sports_Points'],
            'ExxCur_Points': student['ExxCur_Points'],
            'Matches': {}
        }
        
        for term in terms:
            student_dict['Matches'][term] = {
                'Skills': term in student['Technonlogies/Skills known'],
                'Sports': term in student['Sports'],
                'Extracurriculars': term in student['ExtraCurriculum']
            }
        
        students_list.append(student_dict)
    
    return students_list


# ------------------- ROUTES ------------------- #

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/recommend')
def recommend():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('recommend.html')


# @app.route('/submit', methods=['POST'])
# def submit():
#     if 'user' not in session:
#         return redirect(url_for('login'))

#     data = {
#         'S.No': request.form['s_no'],
#         'College Full Name': request.form['college_full_name'],
#         'College City': request.form['college_city'],
#         'Roll No / PRN': request.form['roll_no'],
#         'Prefix': request.form['prefix'],
#         'Candidate Name': request.form['candidate_name'],
#         'Gender': request.form['gender'],
#         'Candidate Mobile Number': request.form['candidate_mobile_number'],
#         'Alternate Mobile Number': request.form.get('alternate_mobile_number', ''),
#         'Primary Email ID (College)': request.form['primary_email'],
#         'Alternate Email ID': request.form.get('alternate_email', ''),
#         '10th Board%': request.form['tenth_board_percentage'],
#         '12th Board%': request.form['twelfth_board_percentage'],
#         'Graduation Degree': request.form['graduation_degree'],
#         'Grad-Specialization': request.form['grad_specialization'],
#         'Graduation CGPA': request.form['graduation_cgpa'],
#         'Year of Graduation': request.form['year_of_graduation'],
#         'Post Graduation Degree': request.form.get('post_graduation_degree', ''),
#         'Post Grad- Specialization': request.form.get('post_grad_specialization', ''),
#         'Post Graduation CGPA': request.form.get('post_graduation_cgpa', ''),
#         'Year of Post Grad': request.form.get('year_of_post_grad', ''),
#         'Foreign Language (Except English)': request.form.get('foreign_language', ''),
#         'Proficiency in foreign language (Beginner / Advanced / Mastery)': request.form.get('foreign_language_proficiency', ''),
#         'Permanent Home Address (Not Campus or Hostel Address)': request.form['permanent_address'],
#         'Permanent City': request.form['permanent_city'],
#         'Permanent State': request.form['permanent_state'],
#         'Permanent Pin Code': request.form['permanent_pin_code'],
#         'Technonlogies/Skills known': request.form['technologies_skills'],
#         'Organization worked with (If Any) Eg: Accenture/KPMG': request.form.get('organization_worked_with', ''),
#         'Prior Experienced (Brief Summary of the work)': request.form.get('prior_experience', ''),
#         'Total Experienced (In Years)': request.form['total_experience'],
#         'Legal pursuit': request.form.get('legal_pursuit', '')
#     }

#     df = pd.DataFrame([data])
#     df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)

#     return "Data submitted successfully!"


@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return redirect(url_for('login'))

    student = Student(
        s_no=request.form['s_no'],
        college_name=request.form['college_full_name'],
        college_city=request.form['college_city'],
        roll_no=request.form['roll_no'],
        prefix=request.form['prefix'],
        name=request.form['candidate_name'],
        gender=request.form['gender'],
        mobile=request.form['candidate_mobile_number'],
        alt_mobile=request.form.get('alternate_mobile_number', ''),
        primary_email=request.form['primary_email'],
        alt_email=request.form.get('alternate_email', ''),
        tenth_percent=request.form['tenth_board_percentage'],
        twelfth_percent=request.form['twelfth_board_percentage'],
        graduation_degree=request.form['graduation_degree'],
        grad_specialization=request.form['grad_specialization'],
        graduation_cgpa=request.form['graduation_cgpa'],
        year_of_graduation=request.form['year_of_graduation'],
        post_graduation_degree=request.form.get('post_graduation_degree', ''),
        post_grad_specialization=request.form.get('post_grad_specialization', ''),
        post_graduation_cgpa=request.form.get('post_graduation_cgpa', ''),
        year_of_post_grad=request.form.get('year_of_post_grad', ''),
        foreign_language=request.form.get('foreign_language', ''),
        foreign_lang_proficiency=request.form.get('foreign_language_proficiency', ''),
        permanent_address=request.form['permanent_address'],
        permanent_city=request.form['permanent_city'],
        permanent_state=request.form['permanent_state'],
        permanent_pin=request.form['permanent_pin_code'],
        skills=request.form['technologies_skills'],
        organization=request.form.get('organization_worked_with', ''),
        prior_experience=request.form.get('prior_experience', ''),
        total_experience=request.form['total_experience'],
        legal_pursuit=request.form.get('legal_pursuit', '')
    )

    db.session.add(student)
    db.session.commit()

    return "Data submitted to the database successfully!"

# recommender for areas of develpment route 
@app.route('/skill_recommend', methods=['POST', 'GET'])
def skill_recommend():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        search_input = request.form['search_input']
        students = unified_student_search(search_input)

        # 💡 Add SkillSkore Booster Tips
        for student in students:
            student['BoosterTips'] = generate_booster_tips(student)

        return render_template('skill_result.html',
                               students=students,
                               search_terms=search_input.split(","))
    return render_template('skill_recommend.html')



# for viewing the database 
@app.route('/students')
def view_students():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    students = Student.query.all()
    return render_template('students.html', students=students)

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'user' not in session:
#         return redirect(url_for('login'))

#     try:
#         # Get values from the form
#         cgpa = float(request.form['graduation_cgpa'])
#         year_grad = int(request.form['year_of_graduation'])
#         experience = float(request.form['total_experience'])
#         skills = request.form['technologies_skills']
#         skill_count = len(skills.split(',')) if skills.strip() else 0

#         lang_level = request.form.get('foreign_language_proficiency', 'Beginner')
#         lang_map = {'Beginner': 0, 'Advanced': 1, 'Mastery': 2}
#         lang_encoded = lang_map.get(lang_level, 0)

#         # Prepare input features
#         features = [[cgpa, year_grad, experience, skill_count, lang_encoded]]
#         scaled_features = scaler.transform(features)

#         # Predict
#         prediction = model_mindset.predict(scaled_features)[0]

#         return render_template('predict_result.html', mindset=prediction)

#     except Exception as e:
#         print("⚠️ Prediction Error:", e)
#         return "Prediction failed. Check input format or try again."

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        # Get form values
        cgpa = float(request.form['graduation_cgpa'])
        year_grad = int(request.form['year_of_graduation'])
        experience = float(request.form['total_experience'])
        skills = request.form['technologies_skills']
        skill_count = len(skills.split(',')) if skills.strip() else 0
        lang_level = request.form.get('foreign_language_proficiency', 'Beginner')
        lang_map = {'Beginner': 0, 'Advanced': 1, 'Mastery': 2}
        lang_encoded = lang_map.get(lang_level, 0)

        features = [[cgpa, year_grad, experience, skill_count, lang_encoded]]
        scaled_features = scaler.transform(features)

        prediction = model_mindset.predict(scaled_features)[0]

        # 👇 Return to recommend.html with prediction
        return render_template('recommend.html', mindset=prediction)

    except Exception as e:
        import traceback
        traceback.print_exc()  # 🔍 Print full traceback in the terminal
        return f"Prediction failed. Error: {str(e)}"


def predict_mindset(form):
    try:
        cgpa = float(form['graduation_cgpa'])
        year_grad = int(form['year_of_graduation'])
        experience = float(form['total_experience'])
        skills = form['technologies_skills']
        skill_count = len(skills.split(','))

        lang_level = form.get('foreign_language_proficiency', 'Beginner')
        lang_map = {'Beginner': 0, 'Advanced': 1, 'Mastery': 2}
        lang_encoded = lang_map.get(lang_level, 0)

        features = [[cgpa, year_grad, experience, skill_count, lang_encoded]]
        scaled = scaler.transform(features)

        prediction = model_mindset.predict(scaled)[0]
        return prediction

    except Exception as e:
        print("Prediction error:", e)
        return None



# recommend for places of concern 
def generate_booster_tips(student):
    tips = []

    try:
        cgpa = float(student['CGPA'])
        if cgpa < 6.5:
            tips.append("Work on improving your CGPA to enhance academic strength.")
    except:
        tips.append("CGPA is missing or invalid.")

    if not student['Skills']:
        tips.append("Consider learning technical skills like Python, SQL, or Web Development.")

    if not student['Sports'] or student['Sports'].strip().lower() in ['no', 'none', '']:
        tips.append("Engaging in sports builds team spirit and leadership skills.")

    if not student['Extracurriculars'] or student['Extracurriculars'].strip().lower() in ['no', 'none', '']:
        tips.append("Participating in extracurriculars shows you're a well-rounded individual.")

    if float(student.get('Total Experience', 0)) == 0:
        tips.append("Try doing internships or real-world projects to build practical experience.")

    return tips




# ------------------- MAIN ------------------- #
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Recreates DB with all current fields
    app.run(debug=True, port=5500)
