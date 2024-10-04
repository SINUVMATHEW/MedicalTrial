import pandas as pd
class Lab:
    def __init__(self, labs_df):
        self.labs_df = labs_df.copy()

    def lab_value_comparison(self,admin_df):
        dummy_year = '2021'
        self.labs_df['DRAW_DATE'] = self.labs_df['DRAW_DATE'] + '-' + dummy_year
        admin_df['Admin Date'] = pd.to_datetime(admin_df['Admin Date'])
        self.labs_df['DRAW_DATE'] = pd.to_datetime(self.labs_df['DRAW_DATE'])
        switched_patients = admin_df.groupby('ID')['Med'].apply(lambda x: list(x)).reset_index()
        switched_patients = switched_patients[switched_patients['Med'].apply(lambda x: x == ['Med A', 'Med B'])]
        switched_ids = switched_patients['ID'].tolist()
        lab_b_values = self.labs_df[self.labs_df['ID'].isin(switched_ids) & (self.labs_df['LAB_RESULT_CODE'] == 'LAB B')]
        average_values = {
            'Medication A': lab_b_values[admin_df['Med'] == 'Med A']['LAB_VALUE'].mean(),
            'Medication B': lab_b_values[admin_df['Med'] == 'Med B']['LAB_VALUE'].mean()
        }

        return average_values

