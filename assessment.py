import pandas as pd

file_path = r'C:\Users\user\Downloads\Air Asia Assessment 1\Sample Data.csv'

# Read csv file
data = pd.read_csv(file_path)

# data set analysis

# Creating separate dataset for Jan 2024 and Jan 2023
Jan_2024 = data[(data['searchdate'] >= '2024-01-01') & (data['searchdate'] <= '2024-01-31')]
print(f"Total Session for Jan 2024 is: {Jan_2024.session.sum()}")  # 3069 sessions for Jan 2024'
print(f"Total Booking for Jan 2024 is:{Jan_2024.booking.sum()}")  # 3069 booking for Jan 2024'

Jan_2023 = data[(data['searchdate'] >= '2023-01-01') & (data['searchdate'] <= '2023-01-31')]
print(f"Total Session for Jan 2023 is: {Jan_2023.session.sum()}")  # 3100 sessions for Jan 2024'
print(f"Total Booking for Jan 2023 is:{Jan_2023.booking.sum()}")  # 3100 booking for Jan 2024'

# Aggregate by year/month

total_sessions_2023 = Jan_2023['session'].sum()
total_bookings_2023 = Jan_2023['booking'].sum()

total_sessions_2024 = Jan_2024['session'].sum()
total_bookings_2024 = Jan_2024['booking'].sum()

# Result check for questions 1 & 2

session_check = total_sessions_2024 > total_sessions_2023
booking_check = total_bookings_2024 > total_bookings_2023

print("Total sessions for Jan2024 is more than Jan2023:", session_check)
print("Total bookings for Jan2024 is more than Jan2023:", booking_check)

# The result confirms number of sessions and bookings are more for Jan 2024 than Jan 2023.

#######################################################################################################

# Found invalid searchdate for the year 2024

data['searchdate'] = pd.to_datetime(data['searchdate'], errors='coerce')
invalid_dates_df = data[data['searchdate'].isna()]

# Count check to validate the thesis

print(f"Count check to confirm if any null values in the date column: {invalid_dates_df.count()}")

# Writing a function for bookings per session calculation
def conversion_rate(data, year, month):
    start_date = pd.Timestamp(year=year, month=month, day=1)
    end_date = start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
    month_data = data[(data['searchdate'] >= start_date) & (data['searchdate'] <= end_date)]

    # Sum total bookings/sessions
    total_bookings = month_data['booking'].sum()
    total_sessions = month_data['session'].sum()

    # Conversion rate calculation
    conversion_rate = total_bookings / total_sessions if total_sessions > 0 else 0

    return conversion_rate


# Result Check

conversion_rate_jan_2023 = conversion_rate(data, 2023, 1)
conversion_rate_jan_2024 = conversion_rate(data, 2024, 1)

print(f"Conversion Rate for Jan 2023: {conversion_rate_jan_2023:.4f}")
print(f"Conversion Rate for Jan 2024: {conversion_rate_jan_2024:.4f}")

# Conversion by country

# Function to aggregate dataframe by grouping country
def Conversion_by_country(df):
    # Group by country and calculate total bookings and sessions
    conversions = df.groupby('country').agg(total_bookings=('booking', 'sum'), total_sessions=('session', 'sum'))
    # Calculate conversion rate
    conversions['conversion_rate'] = conversions['total_bookings'] / conversions['total_sessions']
    return conversions

# Conversion rates for each country by time frame
conversion_rates_2023 = Conversion_by_country(Jan_2023)
conversion_rates_2024 = Conversion_by_country(Jan_2024)

print(conversion_rates_2023.head(1))
print(conversion_rates_2024.head(1))

# Perform simple join for comparison
comparison = conversion_rates_2023.join(conversion_rates_2024, lsuffix='_2023', rsuffix='_2024')

# Change in conversion rate calculation
comparison['conversion_drop'] = comparison['conversion_rate_2023'] > comparison['conversion_rate_2024']

print(comparison)

# Check for all the country by time period
all_dropped = comparison['conversion_drop'].all()
print(f"Has the conversion dropped across all countries from Jan 2023 to Jan 2024? {'Yes' if all_dropped else 'No'}")

# distinct countries

unique_countries_2023 = Jan_2023['country'].nunique()
unique_countries_2024 = Jan_2024['country'].nunique()

print(unique_countries_2023)
print(unique_countries_2024)

# Finding if any differences in the country between two comparison timeframes

countries_2023_set = set(Jan_2023['country'].unique())
countries_2024_set = set(Jan_2024['country'].unique())

# Calculate new and dropped countries
new_countries = countries_2024_set - countries_2023_set
dropped_countries = countries_2023_set - countries_2024_set

print("New countries in Jan 2024:", str(new_countries))
print("Dropped countries in Jan 2024:", str(dropped_countries))

# India is the only country dropped in 2024. Rest all countries are matched.
