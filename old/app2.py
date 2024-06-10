from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import logging

app = Flask(__name__)

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

# Cargar el modelo entrenado
model = joblib.load('rf_rfeModel.pkl')
app.logger.debug('Modelo cargado correctamente.')

@app.route('/')
def home():
    return render_template('rfeModel.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos enviados en el request
        hypertension = int(request.form['hypertension'])
        heart_disease = float(request.form['heart_disease'])
        gender_Female = float(request.form['gender_Female'])
        
        # Crear un DataFrame con los datos
        data_df = pd.DataFrame([[hypertension, heart_disease, gender_Female]], columns=['hypertension', 'heart_disease', 'gender_Female'])
        app.logger.debug(f'DataFrame creado: {data_df}')
        
        # Realizar predicciones
        prediction = model.predict(data_df)
        app.logger.debug(f'Predicción: {prediction[0]}')

        # Convertir la predicción a un tipo de datos nativo de Python
        int_Prediction = int(prediction[0])

        if int_Prediction == 1:
            prediction_result = "una ALTA probabilidad de sufrir un ictus (Enfermedad cerebral)"
        elif int_Prediction == 0:
            prediction_result = "una BAJA posibilidad sufrir un ictus (Enfermedad cerebral)"


        
        # Devolver las predicciones como respuesta JSON
        return jsonify({'categoria': prediction_result})
    except Exception as e:
        app.logger.error(f'Error en la predicción: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

