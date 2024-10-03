class Medication:
    def __init__(self, admin_df):
        self.admin_df = admin_df.copy()


    # Total Monthly Medication Usage:
    # What is the total number of units administered
    # for each medication in each month across all patients?
    def total_monthly_medication_usage(self):
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        aggregated_df = self.admin_df.groupby(['YearMonth','Med'])['Units'].sum().reset_index()
        aggregated_df = aggregated_df.rename(columns={'Units': 'Total Units','YearMonth': 'Month'})
        return aggregated_df


    # How many patients received Medication A and Medication B
    # from July to November?
    def patient_counts_on_each_medication(self, start_month, end_month):
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        filtered_df = self.admin_df[(self.admin_df['YearMonth'] >= start_month) & (self.admin_df['YearMonth'] <= end_month)]
        counted_df = filtered_df.groupby(['YearMonth', 'Med'])['ID'].count().reset_index()
        counted_df = counted_df.rename(columns={'ID': 'Total Patients','YearMonth': 'Month'})
        return counted_df


    # Average Monthly Dose per Patient:
    # What is the average total monthly dose per patient
    # for each medication
    # from July to November?
    def average_monthly_dose_per_patient(self, start_month, end_month):
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        filtered_df = self.admin_df[(self.admin_df['YearMonth'] >= start_month) & (self.admin_df['YearMonth'] <= end_month)]
        counted_df = filtered_df.groupby(['ID', 'YearMonth', 'Med'])['Units'].mean().reset_index()
        counted_df = counted_df.rename(columns={'YearMonth': 'Month', 'ID': 'Total Patients'})
        return counted_df


