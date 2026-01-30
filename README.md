# # CardioCare – Heart Risk Assessment & Awareness Platform


A web-based application built using Flask that helps users assess basic heart disease risk based on health parameters and promotes cardiac awareness.

This project was developed as part of my learning and placement preparation to understand full-stack web development using Python.

--------------------------------------------------

FEATURES

- User Registration and Login
- Session-based Authentication
- Heart Risk Assessment (Low / Medium / High)
- Input Validation for Health Parameters
- Dashboard with Previous Health Records
- High-Risk Alert for Doctor Consultation
- Cardiac Awareness Information Page
- Clean and Responsive UI

--------------------------------------------------

TECH STACK

Backend:
- Python (Flask)

Frontend:
- HTML
- CSS

Database:
- SQLite

Tools:
- VS Code
- GitHub

--------------------------------------------------

PROJECT STRUCTURE

cardiac-awareness-system/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── health.html
│   └── awareness.html
│
└── static/
    └── style.css

--------------------------------------------------

HOW TO RUN THE PROJECT

1. Clone the repository:
   git clone <your-repository-link>

2. Navigate to the project folder:
   cd cardiac-awareness-system

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python app.py

5. Open your browser and visit:
   http://127.0.0.1:5000/

--------------------------------------------------

RISK EVALUATION LOGIC

The system evaluates heart disease risk using the following parameters:
- Blood Pressure
- Blood Sugar Level
- Smoking Habit
- Family History

Based on these inputs, the risk is classified as:
- Low Risk
- Medium Risk
- High Risk

If a High Risk is detected, a warning message is displayed on the dashboard
recommending immediate doctor consultation.

--------------------------------------------------

SECURITY NOTES

- Session-based authentication is implemented
- SQL injection is prevented using parameterized queries
- Input validation is handled at the backend to avoid invalid data storage

--------------------------------------------------

FUTURE ENHANCEMENTS

- Password hashing using bcrypt
- Graphical risk visualization
- Admin analytics dashboard
- Downloadable PDF health reports

--------------------------------------------------

AUTHOR

S.A THARUN
B.Tech – Computer Science and Engineering  
CSE-CTIS
2023-2027