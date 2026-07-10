# Smart Loan Approval Prediction System

A Machine Learning-based web application that predicts whether a loan application is likely to be approved or rejected based on applicant details. The application is built using Python, Flask, and a Random Forest Classifier, and generates a professional PDF report containing the prediction results.

## Live Demo

🔗 https://smart-loan-approval-predictor.onrender.com

## GitHub Repository

🔗 https://github.com/Varsha-k28/Smart_Loan_Approval_Predictor

---

## Features

- Predicts loan approval using Machine Learning.
- Built with Flask and Python.
- Random Forest Classifier for prediction.
- Displays prediction confidence score.
- Displays loan risk level.
- Generates a downloadable PDF report.
- Professional and responsive user interface.
- Personalized suggestions based on prediction.
- Applicant information included in the report.

---

## Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- NumPy
- Pandas
- Joblib

### PDF Generation
- ReportLab

### Deployment
- Render

---

## Project Structure

```text
Smart_Loan_Approval_Predictor/
│
├── app.py
├── train_model.py
├── loan.csv
├── model.pkl
├── education_encoder.pkl
├── self_encoder.pkl
├── status_encoder.pkl
├── requirements.txt
├── Procfile
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## Machine Learning Model

- Algorithm: Random Forest Classifier
- Language: Python
- Library: Scikit-learn
- Model Accuracy: **97.78%**

---

## Input Parameters

- Applicant Name
- Number of Dependents
- Education
- Self Employed
- Annual Income
- Loan Amount
- Loan Term
- CIBIL Score
- Residential Assets Value
- Commercial Assets Value
- Luxury Assets Value
- Bank Asset Value

---

## Output

The application displays:

- Loan Status (Approved / Rejected)
- Prediction Confidence
- Risk Level
- Suggestions
- Downloadable PDF Report

---

## Installation

Clone the repository

```bash
git clone https://github.com/Varsha-k28/Smart_Loan_Approval_Predictor.git
```

Move into the project folder

```bash
cd Smart_Loan_Approval_Predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## Future Enhancements

- User Login and Registration
- Prediction History
- Database Integration
- Admin Dashboard
- Email PDF Report
- Explainable AI
- Cloud Database Support

---

## Author

**Varsha K**

GitHub:
https://github.com/Varsha-k28

Email:
varshabangera5@gmail.com

---

## License

This project is developed for learning and portfolio purposes.
