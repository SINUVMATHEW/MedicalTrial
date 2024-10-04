import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pyparsing import alphas
from Medication import Medication
from Lab import Lab
from src.MedicationA import MedicationA
from src.MedicationB import MedicationB
from src.Patient import Patient
import logging

#Admin.csv is the given DataSet
admin_df = pd.read_csv('data/raw/Admin.csv',thousands=',')
labs_df = pd.read_csv('data/raw/Labs.csv')

#copy of admin_df
cdf = admin_df.copy()
cdf['Admin Date'] = pd.to_datetime(cdf['Admin Date'], format='%d/%m/%Y')
#copy of labs_df
ldf = labs_df.copy()
medication = MedicationA(cdf)
print(f" Unit of Mediaction of A is {medication.findUnit()}")
medication = MedicationB(cdf)
print(f" Unit of Mediaction of B is {medication.findUnit()}")


# 1) Total Monthly Medication Usage:
# What is the total number of units administered
# for each medication in each month across all patients?
medication = Medication(cdf)
try:
    total_monthly_medication_usage = medication.total_monthly_medication_usage()
    print(f"\nTotal Monthly Medication Usage is : \n\n {total_monthly_medication_usage} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 2)Patient Counts on Each Medication:
# How many patients received Medication A and Medication B
# from July to November?
medication = Medication(cdf)
try:
    patient_counts_on_each_medication = medication.patient_counts_on_each_medication('2012-07',
                                                                                     '2012-11')
    print(
        f"\nPatient Counts on Each Medication from July to November is : \n\n {patient_counts_on_each_medication}\n\n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 3)Average Monthly Dose per Patient:
# What is the average total monthly dose per patient
# for each medication
# from July to November?
medication = Medication(cdf)
try:
    average_monthly_dose_per_patient = medication.average_monthly_dose_per_patient('2012-07',
                                                                                   '2012-11')
    print(f"\nAverage Monthly Dose per Patient from July to November is :\n\n {average_monthly_dose_per_patient}\n\n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 4a)Switching Analysis:
# How many patients switched from Medication A to Medication B
# each month (September, October, November)?
medication = Medication(cdf)
try:
    month = '2012-10'
    medication_switched_patients_count = medication.medication_switched_patients_count(month)
    if medication_switched_patients_count.empty:
        print(f"No Medication switch on month {month} ")
    else:
        print(f"\n patients switched from Medication A to Medication B on month {month} is :"
              f"\n\n {medication_switched_patients_count} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 4b)Switching Analysis:
# How many patients started on Medication B
# without being on Medication A in the past?
medication = Medication(cdf)
try:
    month = '2012-11'
    first_time_medication_b_patients_count = medication.first_time_medication_b_patients_count(month)
    if first_time_medication_b_patients_count.empty:
        print(f"No patients started on Medication B without using A in {month} ")
    else:
        print(f"\n patients started on Medication B without using A on month {month} is :"
              f"\n\n {first_time_medication_b_patients_count} \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 5)Time on Medication A Before Switch:
# For patients who switched to Medication B,
# what is the average number of weeks spent on Medication A before switching?
medication = Medication(cdf)
try:
    time_on_medication_a_before_switch = medication.time_on_medication_a_before_switch()
    print(f"\n average number of weeks spent on Medication A before switching is :\n\n "
          f"{time_on_medication_a_before_switch:.2f} Weeks \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# Dose Comparison Before and After Switch:
# 6a) What is the average monthly dose of Medication A for patients before switching to Medication B?
medication = Medication(cdf)
try:
    avg_monthly_dose_of_medication_a_before_b = medication.avg_monthly_dose_of_medication_a_before_b('Med A')
    print(f"\n average monthly dose of Medication A for patients before switching to Medication B :\n\n "
          f"{avg_monthly_dose_of_medication_a_before_b:.2f} Units \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 6b) What is the average monthly dose of Medication B post-switch?
medication = Medication(cdf)
try:
    avg_monthly_dose_of_medication_a_before_b = medication.avg_monthly_dose_of_medication_a_before_b('Med B')
    print(f"\n average monthly dose of Medication B for patients after switching from Medication A :\n\n "
          f"{avg_monthly_dose_of_medication_a_before_b:.2f} Units \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 6c) Breakeven Analysis: If Medication A costs $1 for 100 units,
# what is the breakeven price point for Medication B on a per-unit basis?
medication = Medication(cdf)
n_a = medication.avg_monthly_dose_of_medication_a_before_b('Med A')
cost_per_100_units_a = 1
n_b = medication.avg_monthly_dose_of_medication_a_before_b('Med B')
try:
    breakeven_analysis = medication.breakeven_analysis(n_a, cost_per_100_units_a, n_b)
    print(f"\n breakeven price point for Medication B on a per-unit basis :\n\n "
          f" $ {breakeven_analysis:.3f}  \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 7) Dose Change Over Time:
# How does the average total monthly dose per patient (for both Medication A and B)
# change for patients switched in September vs. October vs. November?
medication = Medication(cdf)
start_month = '2012-09'
end_month = '2012-11'
try:
    average_total_monthly_dose_change = medication.average_total_monthly_dose_change(start_month,end_month)
    print(f"\n average total monthly dose per patient change over month :\n\n "
          f" {average_total_monthly_dose_change}  \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")


# 8a) Second Dose Analysis: For patients switched to Medication B:
# What percentage of the second Medication B dose is the same,
# higher, lower, or zero compared to the first dose?
medication = Medication(cdf)
try:
    second_dose_analysis = medication.second_dose_analysis()
    print(f"\n Second Dose Analysis :\n\n "
          f" {second_dose_analysis}  \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")

# 8b)Lab Value Comparison: For patients that switched from Medication A to B,
# what was the average LAB B value while on Medication A compared to while on Medication B?
lab = Lab(ldf)
try:
    lab_value_comparison = lab.lab_value_comparison(cdf)
    print(f"\n average LAB B value while on Medication A compared to while on Medication B :\n\n "
          f" {lab_value_comparison}  \n \n")
except Exception as e:
    logging.error(f"An error occurred: {e}")
