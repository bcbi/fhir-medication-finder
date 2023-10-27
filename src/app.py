import requests
import os
from flask import Flask, request, render_template
from dotenv import load_dotenv


app = Flask(__name__)

FHIR_SERVER_BASE_URL="http://pwebmedcit.services.brown.edu:8081/fhir"

load_dotenv()

username = os.getenv("FHIR_USERNAME")
password = os.getenv("FHIR_PASSWORD")

def request_medication_list(patient_id, credentials):
    # Use the MedicationRequest or MedicationStatement resource to retrieve medication information.
    req = requests.get(FHIR_SERVER_BASE_URL + f"/MedicationRequest?patient={patient_id}", auth=credentials)

    print(f"Request status: {req.status_code}")

    response = req.json()
    print(response.keys())
    
    return response


@app.route('/', methods=['GET', 'POST'])
def index_eu():
    result = None
    credentials = (username, password)

    if request.method == 'POST':
        try:
            patient_id = request.form['patient_id']
            result = request_medication_list(patient_id, credentials=credentials)
        except ValueError:
            result = 'Invalid input. Please enter a patient ID.'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

