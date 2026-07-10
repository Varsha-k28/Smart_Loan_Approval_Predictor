import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


df = pd.read_csv("loan.csv")

df.columns = df.columns.str.strip()

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()

df.drop(columns=["loan_id"], inplace=True)

education_encoder = LabelEncoder()
self_encoder = LabelEncoder()
status_encoder = LabelEncoder()

df["education"] = education_encoder.fit_transform(df["education"])
df["self_employed"] = self_encoder.fit_transform(df["self_employed"])
df["loan_status"] = status_encoder.fit_transform(df["loan_status"])


X = df.drop("loan_status", axis=1)
y = df["loan_status"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")


print("Education Classes:", education_encoder.classes_)
print("Self Employed Classes:", self_encoder.classes_)
print("Status Classes:", status_encoder.classes_)


joblib.dump(model, "model.pkl")
joblib.dump(education_encoder, "education_encoder.pkl")
joblib.dump(self_encoder, "self_encoder.pkl")
joblib.dump(status_encoder, "status_encoder.pkl")

print("Model Saved Successfully!")