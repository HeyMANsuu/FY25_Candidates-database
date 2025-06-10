# StudySYNC 
# FY25 Candidates Database Web Application

A Flask-based web application for managing, searching, and analyzing student candidate data for the FY25 batch. The app integrates a machine learning model to predict student mindsets and provides skill recommendations and booster tips for student development.

---

## Features

- **Admin Login:** Secure access for administrators.
- **Student Database:** Add, view, and manage student records using SQLite.
- **Skill Search:** Search students by technologies, sports, or extracurricular activities.
- **Skill Recommendations:** Get personalized booster tips for students based on their profiles.
- **Mindset Prediction:** Predict a student's mindset using a trained ML model.
- **Data Storage:** All student data is stored in a local SQLite database and CSV file.
- **Model Integration:** Uses pre-trained models and scalers from the `Models/` directory.

---

## Project Structure

```
FY25_Candidates database/
│
├── app.py
├── FY25_Candidates database.csv
├── Models/
│   ├── mindset_model.pkl
│   ├── scaler.pkl
│   └── ... (other model files)
├── static/
│   ├── img_1.png
│   ├── img_2.png
│   ├── img_3.jpg
│   ├── img.png
│   └── Photo3.jpg
├── templates/
│   ├── home.html
│   ├── login.html
│   └── ... (other HTML templates)
├── FY25_Candidates-database.ipynb
└── README.md
```

---

## Setup Instructions

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**
   ```sh
   pip install flask flask_sqlalchemy pandas numpy scikit-learn
   ```

3. **Ensure model files exist:**
   - Place `mindset_model.pkl` and `scaler.pkl` in the `Models/` directory.

4. **Initialize the database:**
   - Uncomment the following lines in `app.py` to create the database:
     ```python
     # with app.app_context():
     #     db.create_all()
     ```
   - Run the app once, then comment them again to avoid recreating the database.

5. **Run the application:**
   ```sh
   python app.py
   ```
   The app will be available at [http://localhost:5500](http://localhost:5500).

6. **Login Credentials:**
   - Username: `admin`
   - Password: `admin123`

---

## Usage

- **Login:** Go to `/login` to log in as admin.
- **Home:** Main dashboard after login.
- **Add Student:** Use the form to submit new student data.
- **Skill Search:** Use the skill search feature to find students by skills, sports, or extracurriculars.
- **Skill Recommendations:** Get personalized tips for student development.
- **Mindset Prediction:** Submit student details to predict their mindset.

---

## Data

- **Student Data:** Stored in `FY25_Candidates database.csv` and in the SQLite database.
- **CSV Columns:**  
  See [`FY25_Candidates database.csv`](FY25_Candidates%20database.csv) for all fields, including:
  - S.No, College Full Name, College City, Roll No / PRN, Prefix, Candidate Name, Gender, Candidate Mobile Number, Alternate Mobile Number, Primary Email ID (College), Alternate Email ID, 10th Board%, 12th Board%, Graduation Degree, Grad-Specialization, Graduation CGPA, Year of Graduation, Post Graduation Degree, Post Grad- Specialization, Post Graduation CGPA, Year of Post Grad, Foreign Language (Except English), Proficiency in foreign language (Beginner / Advanced / Mastery), Permanent Home Address (Not Campus or Hostel Address), Permanent City, Permanent State, Permanent Pin Code, Technonlogies/Skills known, Tech_points, Organization worked with (If Any) Eg: Accenture/KPMG, Prior Experienced (Brief Summary of the work), Total Experienced (In Years), Legal pursuit, Sports, Sports_Points, ExtraCurriculum, ExxCur_Points

---

## Machine Learning

- **Model:** RandomForestClassifier trained to predict student "Mindset" (Growth, Fixed, Neutral) based on:
  - Graduation CGPA
  - Year of Graduation
  - Total Experience (in years)
  - Skill Count
  - Language Proficiency (Beginner/Advanced/Mastery)
- **Model Files:**  
  - `Models/mindset_model.pkl`  
  - `Models/scaler.pkl`
- **Training Notebook:** See [`FY25_Candidates-database.ipynb`](FY25_Candidates-database.ipynb) for model training and feature engineering.

---

## Templates

- [`templates/login.html`](templates/login.html): Admin login page
- [`templates/home.html`](templates/home.html): Main dashboard
- Other templates: Forms, results, recommendations, etc.

---

## Static Assets

- Images for UI in [`static/`](static/):  
  `img_1.png`, `img_2.png`, `img_3.jpg`, `img.png`, `Photo3.jpg`

---

## License

This project is for educational and internal use only.

---

## Acknowledgements

- Built with [Flask](https://flask.palletsprojects.com/), [SQLAlchemy](https://www.sqlalchemy.org/), [scikit-learn](https://scikit-learn.org/), and [pandas](https://pandas.pydata.org/).
