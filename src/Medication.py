import pandas as pd
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
        filtered_df = self.admin_df[(self.admin_df['YearMonth'] >= start_month)
                                    & (self.admin_df['YearMonth'] <= end_month)]
        counted_df = filtered_df.groupby(['YearMonth', 'Med'])['ID'].count().reset_index()
        counted_df = counted_df.rename(columns={'ID': 'Total Patients','YearMonth': 'Month'})
        return counted_df


    # Average Monthly Dose per Patient:
    # What is the average total monthly dose per patient
    # for each medication
    # from July to November?
    def average_monthly_dose_per_patient(self, start_month, end_month):
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        filtered_df = self.admin_df[(self.admin_df['YearMonth'] >= start_month)
                                    & (self.admin_df['YearMonth'] <= end_month)]
        counted_df = filtered_df.groupby(['ID', 'YearMonth', 'Med'])['Units'].mean().reset_index()
        counted_df = counted_df.rename(columns={'YearMonth':'Month', 'ID':'Total Patients', 'Units':'Average Dosage'})
        return counted_df


    # Switching Analysis:
    # How many patients switched from Medication A to Medication B
    # each month (September, October, November)?
    def medication_switched_patients_count(self, month):
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        self.admin_df = self.admin_df.sort_values(['ID', 'YearMonth'])
        self.admin_df['Switched'] = (self.admin_df['Med'] == 'Med B') & (self.admin_df['Med'].shift(1) == 'Med A') & (
                    self.admin_df['ID'] == self.admin_df['ID'].shift(1))
        switch_count = self.admin_df[self.admin_df['Switched']].groupby('YearMonth').size().reset_index(
            name='Patients Switched')
        result = switch_count[switch_count['YearMonth'] == month]
        return result


    #How many patients started on Medication B
    # without being on Medication A in the past?
    def first_time_medication_b_patients_count(self, month):
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        self.admin_df = self.admin_df.sort_values(['ID', 'YearMonth'])
        self.admin_df['UniqueB'] = (self.admin_df['Med'] == 'Med B') & (self.admin_df['Med'].shift(1) != 'Med A') & (
                self.admin_df['ID'] == self.admin_df['ID'].shift(1))
        unique_count = self.admin_df[self.admin_df['UniqueB']].groupby('YearMonth').size().reset_index(
            name='Patients only used B')
        result = unique_count[unique_count['YearMonth'] == month]
        return result


    # Time on Medication A Before Switch:
    # For patients who switched to Medication B,
    # what is the average number of weeks spent on Medication A before switching?
    def time_on_medication_a_before_switch(self):
        df_weeks_spent = self.admin_df.groupby('ID').apply(self.weeks_on_med_a_before_switch).dropna().reset_index()
        df_weeks_spent.columns = ['ID', 'Weeks on Med A Before Switching']
        average_weeks = df_weeks_spent['Weeks on Med A Before Switching'].mean()
        return average_weeks


    def weeks_on_med_a_before_switch(self, group):
        group = group.sort_values(['Admin Date'])
        med_b_date = group[group['Med'] == 'Med B']['Admin Date'].min()
        if pd.notna(med_b_date):
            med_a_start = group[group['Med'] == 'Med A']['Admin Date'].min()
            weeks_spent = (med_b_date - med_a_start).days / 7
            return weeks_spent
        else:
            return None


    # What is the average monthly dose of Medication A
    # for patients before switching to Medication B?
    # What is the average monthly dose of Medication B post-switch?
    # --med is the Medication to be calculated
    def avg_monthly_dose_of_medication_a_before_b(self,med):
        patients_switched = self.admin_df.groupby('ID')['Med'].apply(lambda meds: {'Med A',
                                                                                   'Med B'}.issubset(set(meds)))
        df_switched = self.admin_df[self.admin_df['ID'].isin(patients_switched[patients_switched].index)]
        df_med_a_before_switch = df_switched[df_switched['Med'] == med].copy()
        df_med_a_before_switch['Month'] = df_med_a_before_switch['Admin Date'].dt.to_period('M')
        monthly_dose = df_med_a_before_switch.groupby(['ID', 'Month'])['Units'].sum().reset_index()
        average_monthly_dose = monthly_dose.groupby('ID')['Units'].mean().reset_index()
        average_monthly_dose.columns = ['ID', 'Average Monthly Dose Before Switch']
        overall_average_monthly_dose = average_monthly_dose['Average Monthly Dose Before Switch'].mean()
        return overall_average_monthly_dose


    # How does the average total monthly dose per patient (for both Medication A and B)
    # change for patients switched in September vs. October vs. November?
    def breakeven_analysis(self,n_a, cost_per_100_units_a, n_b):
        cost_per_unit_a = cost_per_100_units_a / 100
        breakeven_price_b = (n_a * cost_per_unit_a) / n_b
        return breakeven_price_b


    # How does the average total monthly dose per patient (for both Medication A and B)
    # change for patients switched in September vs. October vs. November?
    def average_total_monthly_dose_change(self,start_month,end_month):

        self.admin_df['Admin Date'] = pd.to_datetime(self.admin_df['Admin Date'], errors='coerce')
        self.admin_df['YearMonth'] = self.admin_df['Admin Date'].dt.to_period('M')
        switch_months = pd.period_range(start_month, end_month, freq='M')
        filtered_df = self.admin_df[self.admin_df['YearMonth'].isin(switch_months)]
        monthly_dose = filtered_df.groupby(['YearMonth', 'Med'])['Units'].sum().reset_index()
        total_patients = filtered_df.groupby(['YearMonth', 'Med'])['ID'].nunique().reset_index()
        total_patients = total_patients.rename(columns={'ID': 'Total Patients'})
        monthly_dose = pd.merge(monthly_dose, total_patients, on=['YearMonth', 'Med'], how='left')
        monthly_dose['Avg Monthly Dose Per Patient'] = monthly_dose['Units'] / monthly_dose['Total Patients']
        return monthly_dose


    def second_dose_analysis(self):
        self.admin_df['Switched'] = self.admin_df.apply(lambda row: row['Med'] == 'Med B' and row['ID'] in
                        self.admin_df[self.admin_df['Med'] == 'Med A']['ID'].values, axis=1)
        switched_patients_df = self.admin_df[self.admin_df['Switched'] == True].copy()
        switched_to_med_b_df = switched_patients_df[switched_patients_df['Med'] == 'Med B']
        switched_to_med_b_df = switched_to_med_b_df.sort_values(['ID', 'Admin Date'])
        switched_to_med_b_df['Dose Rank'] = switched_to_med_b_df.groupby('ID').cumcount() + 1
        dose_comparison_df = switched_to_med_b_df.pivot(index='ID', columns='Dose Rank', values='Units').reset_index()
        dose_columns = ['ID'] + [f'Dose {i}' for i in range(1, dose_comparison_df.shape[1])]
        dose_comparison_df.columns = dose_columns
        if len(dose_columns) == 3:
            dose_comparison_df.columns = ['ID', 'First Dose', 'Second Dose']
        elif len(dose_columns) == 2:
            dose_comparison_df.columns = ['ID', 'First Dose']
        def classify_dose(first, second):
            if pd.isna(second):
                return 'No Second Dose'
            elif second == 0:
                return 'Zero Dose'
            elif second == first:
                return 'Same'
            elif second > first:
                return 'Higher'
            else:
                return 'Lower'
        if 'Second Dose' in dose_comparison_df.columns:
            dose_comparison_df['Second Dose Classification'] = dose_comparison_df.apply(
                lambda row: classify_dose(row['First Dose'], row.get('Second Dose', None)), axis=1
            )
        else:
            dose_comparison_df['Second Dose Classification'] = 'No Second Dose'

        classification_counts = dose_comparison_df['Second Dose Classification'].value_counts(normalize=True) * 100
        return self.admin_df
