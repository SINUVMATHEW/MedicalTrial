import pandas as pd

admin_df = pd.read_csv('data/raw/Admin.csv')

class Patient:
    def __init__(self,id):
        self.id = id

    def medicine_record(self):
        patient_record = admin_df[admin_df['ID'] == self.id]
        if not patient_record.empty:
            return patient_record
        else:
            return f"No record found for Patient ID: {self.id}"


patient1 = Patient(5)
print(patient1.medicine_record())