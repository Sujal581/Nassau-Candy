import pandas as pd


def load_data(file):
    df = pd.read_csv(file)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
    return df


def clean_data(df):
    df = df.dropna(subset=['Order Date', 'Ship Date'])
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df = df[df['Lead Time'] >= 0]
    return df


def feature_engineering(df, save=False, path="final_cleaned_data.csv"):
    if 'Division' in df.columns and 'State/Province' in df.columns:
        df['Route'] = df['Division'].astype(str) + " → " + df['State/Province'].astype(str)
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
    result['Avg_Lead_Time'] = result['Avg_Lead_Time'].round(1).fillna(0)
    result['Delay_Rate'] = (result['Delay_Rate'] * 100).round(1).fillna(0)
    return result.sort_values(by='Avg_Lead_Time')


def geo_analysis(df):
    result = df.groupby('State/Province').agg(
        Avg_Lead_Time=('Lead Time', 'mean'),
        Shipments=('Order ID', 'count')
    ).reset_index()
    result['Avg_Lead_Time'] = result['Avg_Lead_Time'].round(1).fillna(0)
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


def division_analysis(df):
    result = df.groupby('Division').agg(
        Shipments=('Order ID', 'count'),
        Avg_Lead=('Lead Time', 'mean'),
        Delay_Rate=('Delayed', 'mean'),
        States=('State/Province', 'nunique')
    ).reset_index()
    result['Avg_Lead'] = result['Avg_Lead'].round(1)
    result['Delay_Rate'] = (result['Delay_Rate'] * 100).round(1)
    result['Risk_Score'] = (result['Avg_Lead'] * 0.5 + result['Delay_Rate'] * 0.5).round(1)
    return result
