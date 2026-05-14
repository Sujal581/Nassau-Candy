import pandas as pd

def load_data(file):
    df = pd.read_csv(file)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce').dt.date
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce').dt.date
    return df

def clean_data(df):
    df = df.dropna(subset=['Order Date', 'Ship Date'])
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df = df[df['Lead Time'] >= 0]
    return df

def feature_engineering(df, save=True, path="final_cleaned_data.csv"):
    df['Route'] = df['Division'] + " → " + df['State/Province']
    df['Delayed'] = df['Lead Time'] > 5
    if save:
        df.to_csv(path, index=False)
    return df

def route_analysis(df):
    result = df.groupby('Route').agg(
        Avg_Lead_Time=('Lead Time', 'mean'),
        Total_Shipments=('Order ID', 'count'),
        Delay_Rate=('Delayed', 'mean')
    ).reset_index()
    result['Avg_Lead_Time'] = result['Avg_Lead_Time'].round(0).astype(int)
    result['Delay_Rate'] = (result['Delay_Rate'] * 100).round(0).astype(int)
    return result.sort_values(by='Avg_Lead_Time')

def geo_analysis(df):
    result = df.groupby('State/Province').agg(
        Avg_Lead_Time=('Lead Time', 'mean'),
        Shipments=('Order ID', 'count')
    ).reset_index()
    result['Avg_Lead_Time'] = result['Avg_Lead_Time'].round(0).astype(int)
    return result

def ship_mode_analysis(df):
    result = df.groupby('Ship Mode').agg(
        Avg_Lead_Time=('Lead Time', 'mean'),
        Shipments=('Order ID', 'count'),
        Delay_Rate=('Delayed', 'mean')
    ).reset_index()
    result['Avg_Lead_Time'] = result['Avg_Lead_Time'].round(1)
    result['Delay_Rate'] = (result['Delay_Rate'] * 100).round(1)
    return result
