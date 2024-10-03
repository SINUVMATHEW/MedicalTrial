import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pyparsing import alphas

from Medication import Medication
from src.Patient import Patient
import logging


admin_df = pd.read_csv('data/raw/Admin.csv',thousands=',')
labs_df = pd.read_csv('data/raw/Labs.csv')

#copy of admin_df
cdf = admin_df.copy()
cdf['Admin Date'] = pd.to_datetime(cdf['Admin Date'], format='%d/%m/%Y')

# 1) Total Monthly Medication Usage:
# What is the total number of units administered
# for each medication in each month across all patients?
medication = Medication(cdf)
try:
    total_monthly_medication_usage = medication.total_monthly_medication_usage()
    print(f"\nTotal Monthly Medication Usage is : \n\n {total_monthly_medication_usage} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


#2)Patient Counts on Each Medication:
# How many patients received Medication A and Medication B
# from July to November?
medication = Medication(cdf)
try:
    patient_counts_on_each_medication = medication.patient_counts_on_each_medication('2012-07', '2012-11')
    print(
        f"\nPatient Counts on Each Medication from July to November is : \n\n {patient_counts_on_each_medication} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


#3)Average Monthly Dose per Patient:
# What is the average total monthly dose per patient
# for each medication
# from July to November?
medication = Medication(cdf)
try:
    average_monthly_dose_per_patient = medication.average_monthly_dose_per_patient('2012-07', '2012-11')
    print(f"\nAverage Monthly Dose per Patient from July to November is :\n\n {average_monthly_dose_per_patient} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")

#4a)Switching Analysis:
# How many patients switched from Medication A to Medication B
# each month (September, October, November)?
medication = Medication(cdf)
try:
    average_monthly_dose_per_patient = medication.average_monthly_dose_per_patient('2012-07', '2012-11')
    print(f"\nAverage Monthly Dose per Patient from July to November is :\n\n {average_monthly_dose_per_patient} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")





#visualization
    # plt.figure(figsize=(12,10))  # Set the figure size
    # sns.barplot(data=total_monthly_medication_usage, x='YearMonth', y='Total Units', hue='Med', dodge=True, alpha=0.7)
    # plt.title('Total Units Administered for Each Medication per Month')
    # plt.ylabel('Total Units')
    # plt.xlabel('Year-Month')
    # plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    # plt.show()