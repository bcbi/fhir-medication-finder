from flask import Flask, request, render_template
from dotenv import load_dotenv
from fhir_utils import get_fhir_credentials, request_medication_list, request_condition_list

app = Flask(__name__)

load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index_eu():
    result = None
    credentials = get_fhir_credentials()

    if request.method == 'POST':
        try:
            patient_id = request.form['patient_id']
            medication_request_result, patient_result = request_medication_list(patient_id, credentials=credentials)
            condition_result = request_condition_list(patient_id, credentials=credentials)

            result = {
                'medication_request': medication_request_result,
                'patient': patient_result,
                'condition': condition_result
            }
        except ValueError:
            result = 'Invalid input. Please enter a patient ID.'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)