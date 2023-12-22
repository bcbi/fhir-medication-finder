import requests
import os

FHIR_SERVER_BASE_URL = "http://pwebmedcit.services.brown.edu:8081/fhir"

def get_fhir_credentials():
    """
    Get FHIR server credentials from environment variables.
    """
    username = os.getenv("FHIR_USERNAME")
    password = os.getenv("FHIR_PASSWORD")
    return (username, password)

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

    if 'entry' in medication_request_response:
        return medication_request_response, patient_response
    else:
        raise ValueError("Invalid response format for medication request.")



def request_condition_list(patient_id, credentials):
    condition_url = f"{FHIR_SERVER_BASE_URL}/Condition?patient={patient_id}"
    condition_req = requests.get(condition_url, auth=credentials)
    
    print(f"Condition status: {condition_req.status_code}")
    
    condition_response = condition_req.json()
    
    print(condition_response.keys())
    
    return condition_response
