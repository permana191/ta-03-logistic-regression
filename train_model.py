import pandas as pd
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, roc_curve, roc_auc_score
from imblearn.over_sampling import SMOTE

# 1. Load Data & Fitur Seleksi
df = pd.read_csv('dataset/data.csv')
target = 'Bankrupt?'

# Memilih 5 fitur terpenting untuk kemudahan input web
features = [
    ' ROA(C) before interest and depreciation before interest',
    ' Debt ratio %',
    ' Net Income to Total Assets',
    ' Working Capital to Total Assets',
    ' Cash/Total Assets'
]

X = df[features]
y = df[target]

# 2. Split & SMOTE
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

# 3. Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_sm)
X_test_scaled = scaler.transform(X_test)

# 4. Training
model = LogisticRegression(solver='lbfgs', random_state=42)
model.fit(X_train_scaled, y_train_sm)

# 5. Evaluasi & Ekspor Metrik
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

metrics = {
    "accuracy": model.score(X_test_scaled, y_test),
    "roc_auc": roc_auc_score(y_test, y_pred_proba)
}
with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)

# 6. Visualisasi (Sesuai output folder)
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Aman', 'Bangkrut'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('Figure_1.png')
plt.close()

fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
plt.figure()
plt.plot(fpr, tpr, color='orange', label=f'AUC = {metrics["roc_auc"]:.2f}')
plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.savefig('Figure_2.png')
plt.close()

# 7. Simpan Model
joblib.dump(model, 'models/model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("Model dan visualisasi berhasil disimpan!")