def calculate_health_kpis(df, age_col, bmi_col, disease_col):
    total_patients = len(df)
    disease_rate = df[disease_col].mean() * 100
    avg_age = df[age_col].mean()
    high_risk = df[df[bmi_col] > 30].shape[0]

    return total_patients, disease_rate, avg_age, high_risk
