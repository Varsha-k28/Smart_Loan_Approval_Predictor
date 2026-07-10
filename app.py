from flask import Flask, render_template, request
import joblib
import numpy as np
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
import io
from datetime import datetime
import uuid
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=24,
    textColor=HexColor("#0096D6"),
    alignment=TA_CENTER,
    spaceAfter=20
)
heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=15,
    textColor=HexColor("#005B96"),
    spaceBefore=12,
    spaceAfter=10

)
body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=11,
    leading=20,
    spaceAfter=6
)

info_style = ParagraphStyle(
    "InfoStyle",
    parent=body_style,
    alignment=TA_CENTER,
    fontSize=10,
    textColor=HexColor("#555555")
)

footer_style = ParagraphStyle(
    "FooterStyle",
    parent=body_style,
    alignment=TA_CENTER,
    textColor=HexColor("#666666"),
    fontSize=10,
    spaceBefore=20
)

disclaimer_style=ParagraphStyle(
    "DisclaimerStyle",
    parent=footer_style,
    fontSize=8,
    textColor=HexColor("#777777"),
    leading=12
)

app = Flask(__name__)

model = joblib.load("model.pkl")
education_encoder = joblib.load("education_encoder.pkl")
print("Education Classes:", education_encoder.classes_)

self_encoder = joblib.load("self_encoder.pkl")
print("Self Employed Classes:", self_encoder.classes_)

status_encoder = joblib.load("status_encoder.pkl")
print("Status Classes:", status_encoder.classes_)


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None
    eligibility_score = None
    risk = None
    form_data = {}

    if request.method == "POST":

        form_data = request.form

        no_of_dependents = int(request.form["no_of_dependents"])
        education = education_encoder.transform([request.form["education"]])[0]
        self_employed = self_encoder.transform([request.form["self_employed"]])[0]
        income_annum = int(request.form["income_annum"])
        loan_amount = int(request.form["loan_amount"])
        loan_term = int(request.form["loan_term"])
        cibil_score = int(request.form["cibil_score"])
        residential_assets_value = int(request.form["residential_assets_value"])
        commercial_assets_value = int(request.form["commercial_assets_value"])
        luxury_assets_value = int(request.form["luxury_assets_value"])
        bank_asset_value = int(request.form["bank_asset_value"])

        features = np.array([[
            no_of_dependents,
            education,
            self_employed,
            income_annum,
            loan_amount,
            loan_term,
            cibil_score,
            residential_assets_value,
            commercial_assets_value,
            luxury_assets_value,
            bank_asset_value
        ]])

        result = model.predict(features)
        prediction = status_encoder.inverse_transform(result)[0]

        probability = model.predict_proba(features)
        confidence = round(max(probability[0]) * 100, 2)

        eligibility_score = confidence

        if confidence >= 90:
            risk = "Low"
        elif confidence >= 75:
            risk = "Medium"
        else:
            risk = "High"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        eligibility_score=eligibility_score,
        risk=risk,
        applicant_name=form_data.get("applicant_name", ""),
        form_data=form_data
    )
@app.route("/download")
def download():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
    buffer,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)
    story = []

    story.append(Paragraph("SMART LOAN APPROVAL PREDICTION REPORT", title_style))
    report_id=str(uuid.uuid4())[:8].upper()
    
    story.append(Paragraph(f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",info_style))
    story.append(Paragraph(f"<b>Report ID:</b> {report_id}",info_style))
    story.append(Paragraph("<font color='#0096D6'>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</font>",info_style))
    story.append(Paragraph("<br/>",body_style))


    story.append(Paragraph("Applicant Information", heading_style))
    story.append(Paragraph(f"<b>Applicant Name:</b> {request.args.get('applicant_name')}", body_style))
    story.append(Paragraph(f"<b>Dependents:</b> {request.args.get('no_of_dependents')}", body_style))
    story.append(Paragraph(f"<b>Education:</b> {request.args.get('education')}", body_style))
    story.append(Paragraph(f"<b>Self Employed:</b> {request.args.get('self_employed')}", body_style))
    story.append(Paragraph(f"<b>Annual Income:</b> INR {int(request.args.get('income_annum', 0)):,}", body_style))
    story.append(Paragraph(f"<b>Loan Amount:</b> INR {int(request.args.get('loan_amount', 0)):,}", body_style))
    story.append(Paragraph(f"<b>Loan Term:</b> {request.args.get('loan_term')} Years", body_style))
    story.append(Paragraph(f"<b>CIBIL Score:</b> {request.args.get('cibil_score')}", body_style))
    story.append(Paragraph(f"<b>Residential Assets:</b> INR {int(request.args.get('residential_assets_value', 0)):,}", body_style))
    story.append(Paragraph(f"<b>Commercial Assets:</b> INR {int(request.args.get('commercial_assets_value', 0)):,}", body_style))
    story.append(Paragraph(f"<b>Luxury Assets:</b> INR {int(request.args.get('luxury_assets_value', 0)):,}", body_style))
    story.append(Paragraph(f"<b>Bank Assets:</b> INR {int(request.args.get('bank_asset_value', 0)):,}", body_style))
    story.append(Paragraph("<font color='#0096D6'>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</font>",body_style))
    story.append(Paragraph("<br/>",body_style))

    story.append(Paragraph("Prediction Result", heading_style))

    prediction = request.args.get("prediction")

    if prediction == "Approved":
        prediction_text = "<font color='green'><b>APPROVED</b></font>"
    else:
        prediction_text = "<font color='red'><b>REJECTED</b></font>"

    story.append(Paragraph(f"<b>Prediction:</b> {prediction_text}", body_style))
    story.append(Paragraph(f"<b>Prediction Confidence:</b> {request.args.get('confidence')}%",body_style))
    risk = request.args.get("risk")

    if risk == "Low":
        risk_text = "<font color='green'><b>Low</b></font>"
    elif risk == "Medium":
        risk_text = "<font color='orange'><b>Medium</b></font>"
    else:
        risk_text = "<font color='red'><b>High</b></font>"

    story.append(Paragraph(f"<b>Risk Level:</b> {risk_text}", body_style))
    story.append(Paragraph("<br/>", body_style))
    story.append(Paragraph("<font color='#0096D6'>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</font>",body_style))
    story.append(Paragraph("<br/>",body_style))

    if prediction == "Approved":
        story.append(Paragraph("Suggestions", heading_style))
        story.append(Paragraph("• Congratulations! Your loan application is likely to be approved.", body_style))
        story.append(Paragraph("• Maintain your current CIBIL score.", body_style))
        story.append(Paragraph("• Continue managing your income and expenses responsibly.", body_style))
        story.append(Paragraph("• Make timely repayments to maintain a healthy credit history.", body_style))
        story.append(Paragraph("• Keep your financial documents updated for faster loan processing.", body_style))
    else:
        story.append(Paragraph("Suggestions for Improvement", heading_style))
        story.append(Paragraph("• Improve your CIBIL score by paying EMIs and credit card bills on time.", body_style))
        story.append(Paragraph("• Increase your annual income before reapplying.", body_style))
        story.append(Paragraph("• Consider requesting a lower loan amount.", body_style))
        story.append(Paragraph("• Increase your savings or asset value to improve eligibility.", body_style))
        story.append(Paragraph("• Reduce existing debts to improve your repayment capacity.", body_style))

    story.append(Paragraph("<br/>", body_style))
    story.append(Paragraph("Generated by Smart Loan Approval Prediction System", footer_style))
    story.append(Paragraph("<br/>",body_style))

    story.append(Paragraph("<b>Disclaimer:</b> This prediction is generated using a Machine Learning model for learning purposes and should not be considered as an official loan approval decision by any financial institution.",disclaimer_style))

    doc.build(story)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Loan_Approval_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)