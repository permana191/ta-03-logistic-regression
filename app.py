from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model dan scaler
try:
    model = joblib.load('models/model.pkl')
    scaler = joblib.load('models/scaler.pkl')
except:
    print("Peringatan: File model.pkl atau scaler.pkl belum ada. Latih model terlebih dahulu.")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', submitted=False)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Ambil nilai dari form
            form_data = {
                'roa': float(request.form['roa']),
                'debt_ratio': float(request.form['debt_ratio']),
                'net_income': float(request.form['net_income']),
                'working_capital': float(request.form['working_capital']),
                'cash_assets': float(request.form['cash_assets'])
            }
            
            # Format array untuk prediksi
            features = np.array([[
                form_data['roa'], 
                form_data['debt_ratio'], 
                form_data['net_income'], 
                form_data['working_capital'], 
                form_data['cash_assets']
            ]])
            
            features_scaled = scaler.transform(features)
            
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0][1] * 100
            
            # Tentukan status dan kelas warna UI
            if prediction == 1:
                result_text = "Tinggi (Berisiko Bangkrut)"
                status_class = "danger"
            else:
                result_text = "Rendah (Perusahaan Aman)"
                status_class = "success"
                
            return render_template('index.html', 
                                   submitted=True, 
                                   result_text=result_text, 
                                   probability=round(probability, 2),
                                   status_class=status_class,
                                   form_data=form_data)
        except Exception as e:
            return render_template('index.html', submitted=False, error="Harap masukkan angka yang valid.")

if __name__ == '__main__':
    app.run(debug=True)