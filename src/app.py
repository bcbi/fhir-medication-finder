import requests
import os
from flask import Flask, request, render_template
from dotenv import load_dotenv

app = Flask(__name__)

FHIR_SERVER_BASE_URL = "http://pwebmedcit.services.brown.edu:8081/fhir"

load_dotenv()

username = os.getenv("FHIR_USERNAME")
password = os.getenv("FHIR_PASSWORD")

def request_medication_list(patient_id, credentials):
    medication_request_url = f"{FHIR_SERVER_BASE_URL}/MedicationRequest?patient={patient_id}"
    patient_url = f"{FHIR_SERVER_BASE_URL}/Patient/{patient_id}"

    # Make separate requests for MedicationRequest and Patient
    medication_request_req = requests.get(medication_request_url, auth=credentials)
    patient_req = requests.get(patient_url, auth=credentials)

    print(f"Medication Request status: {medication_request_req.status_code}")
    print(f"Patient status: {patient_req.status_code}")

    medication_request_response = medication_request_req.json()
    patient_response = patient_req.json()

    print(medication_request_response.keys())
    print(patient_response.keys())

    return medication_request_response, patient_response

@app.route('/', methods=['GET', 'POST'])
def index_eu():
    result = None
    credentials = (username, password)

    if request.method == 'POST':
        try:
            patient_id = request.form['patient_id']
            medication_request_result, patient_result = request_medication_list(patient_id, credentials=credentials)
            # Combine information from MedicationRequest and Patient as needed
            result = {
                'medication_request': medication_request_result,
                'patient': patient_result
            }
        except ValueError:
            result = 'Invalid input. Please enter a patient ID.'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
