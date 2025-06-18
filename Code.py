# -----------------------------------------------------------
# Analysis of Fuel Prices in WA using FuelWatch database
# -----------------------------------------------------------
# PYTHON CODE
# -----------------------------------------------------------


# SECTION 1 - SETTING UP TO ANALYSE THE DATASET
# -----------------------------------------------------------

# Required Modules
import math
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Working Directory Check
print("Working Directory: ", os.getcwd())

# Input Dataset file 
WA_fuel_df = pd.read_csv("E:/UWA/PFB/GroupAssign/WA_fuel_data.csv")


# SECTION 2 - EXPLORING, CLEANING & PRE-PROCESSING THE DATASET
# ----------------------------------------------------------

# Exploring the Fuel Prices Dataset
print(WA_fuel_df.head())
print(WA_fuel_df.columns)
print(WA_fuel_df.index)

# Check and Drop rows with missing values
print(WA_fuel_df.isna())
WA_fuel_df = WA_fuel_df.dropna()

# Summary statistics of the Dataset
print(WA_fuel_df.describe)

# Converting the publish_date column to datetime format
WA_fuel_df['publish_date'] = pd.to_datetime(WA_fuel_df['publish_date'])

# Creating new columns for grouping - Monthly and Weekly
WA_fuel_df['month'] = WA_fuel_df['publish_date'].dt.strftime('%Y-%m')
WA_fuel_df['week'] = WA_fuel_df['publish_date'].dt.strftime('%Y-%U')

# Standardise text case
WA_fuel_df['brand_description'] = WA_fuel_df['brand_description'].str.capitalize()
WA_fuel_df['product_description'] = WA_fuel_df['product_description'].str.upper()


# SECTION 3 - ANALYSIS OF THE WA FUEL PRICE DATASET
# ----------------------------------------------------------

# 1. Average Price per Fuel Type for each Month

monthly_avg_prices = WA_fuel_df.groupby(['month', 'product_description'])['product_price']
monthly_avg_prices = monthly_avg_prices.mean().reset_index()
print("\n\tAverage Price per Fuel Type for each Month\n")
print(monthly_avg_prices)

# Plotted as a line graph to understand insights
plt.figure(figsize=(12, 6))

# Get unique fuel types
fuel_types = monthly_avg_prices['product_description'].unique()

# Plotting each fuel type as a separate line
for fuel in fuel_types:
    fuel_data = monthly_avg_prices[monthly_avg_prices['product_description'] == fuel]
    plt.plot(fuel_data['month'], fuel_data['product_price'], label=fuel)

# Format chart
plt.title("Monthly Price Trends for Each Fuel Type")
plt.xlabel("Month")
plt.ylabel("Average Price (cents/litre)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title="Fuel Type")
plt.tight_layout()
plt.show()

# 2. Highest and Lowest Price for each Fuel Type

fuel_price_high_low = []

for fuel in WA_fuel_df['product_description'].unique():
    fuel_index = WA_fuel_df[WA_fuel_df['product_description'] == fuel]
    
    highest_fuel_price = fuel_index['product_price'].max()
    lowest_fuel_price = fuel_index['product_price'].min()
    
    high_fuel_date = fuel_index[fuel_index['product_price'] == highest_fuel_price].iloc[0]
    low_fuel_date = fuel_index[fuel_index['product_price'] == lowest_fuel_price].iloc[0]

    fuel_price_high_low.append(
        {
        'Fuel Type': fuel,
        'Max Fuel Price': highest_fuel_price,
        'Max Fuel Date': high_fuel_date['publish_date'].date(),
        'Min Fuel Price': lowest_fuel_price,
        'Min Fuel Date': low_fuel_date['publish_date'].date()
        }
    )
    
fuel_price_high_low_df = pd.DataFrame(fuel_price_high_low)
print("\n\tHighest and Lowest Price for each Fuel Type\n")
print(fuel_price_high_low_df)


# 3. Price Analysis for a particular Fuel for each Region throughout WA (Monthly)
#    Chosen Fuel type: Diesel

diesel_data = WA_fuel_df[WA_fuel_df['product_description'] == 'DIESEL']

diesel_monthly_avg_region = diesel_data.groupby(['month', 'region_description'])['product_price']
diesel_monthly_avg_region = diesel_monthly_avg_region.mean().reset_index()
print("\n\tMonthly Average Diesel Prices by Region\n")
print(diesel_monthly_avg_region)

diesel_region_high_low = []

for region in diesel_data['region_description'].unique():
    region_data = diesel_data[diesel_data['region_description'] == region]

    highest_price = region_data['product_price'].max()
    lowest_price = region_data['product_price'].min()

    highest_price_date = region_data[region_data['product_price'] == highest_price].iloc[0]
    lowest_price_date = region_data[region_data['product_price'] == lowest_price].iloc[0]

    diesel_region_high_low.append(
        {
        'Region': region,
        'Max Price': highest_price,
        'Max Date': highest_price_date['publish_date'].date(),
        'Min Price': lowest_price,
        'Min Date': lowest_price_date['publish_date'].date()
        }
    )
    
diesel_region_high_low_df = pd.DataFrame(diesel_region_high_low)
print("\n\tHighest and Lowest Price for Diesel by Region\n")
print(diesel_region_high_low_df)


# 4. Price analysis for all Fuel Types in two Selected Brands (Weekly)
#    Chosen Brands: Puma and Vibe

selected_brands_df = WA_fuel_df[(WA_fuel_df['brand_description'] == 'Puma') | (WA_fuel_df['brand_description'] == 'Vibe')]

# Group weekly data for each brand and fuel type
weekly_brand_prices = selected_brands_df.groupby(['brand_description', 'week', 'product_description'])['product_price']
weekly_brand_prices = weekly_brand_prices.mean().reset_index()

# Plotting Function
def plot_brand_weekly_trends(brand):
    """This plotting function is for weekly trend line per fuel"""
    brand_data = weekly_brand_prices[weekly_brand_prices['brand_description'] == brand]
    plt.figure(figsize=(12, 6))
    
    for fuel in brand_data['product_description'].unique():
        fuel_data = brand_data[brand_data['product_description'] == fuel]
        plt.plot(fuel_data['week'], fuel_data['product_price'], label=fuel)
        
    plt.title(brand + " Weekly Fuel Prices")
    plt.xlabel('Week')
    plt.ylabel('Price (cents)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Generate plots for Puma and Vibe
plot_brand_weekly_trends("Puma")
plot_brand_weekly_trends("Vibe")

# Price scale tick reference
print("\nPrice tick intervals (rounded):")
price_ticks = list(range(0, math.ceil(WA_fuel_df['product_price'].max()), 10))
print(price_ticks)


# 5. Interpretation of the change in Fuel Price over time
#    with various Fuel Types and between Puma and Vibe brands
#         Diesel remained consistently priced; premium fuels like 98 RON showed volatility.
#         Puma priced higher with stability; Vibe remained low-cost but steady.
#         Both brands followed market trends, not reactive pricing changes


# 6. Challenges, Solutions and useful input from the analysis
#    for Business Decision Making
#         Grouping time-series data was tricky; solved using .strftime() and standardised labels.
#         Plotting multiple fuel types clearly was difficult; improved using matplotlib formatting.
#         Final insights help retailers plan fuel strategy, pricing, and inventory decisions.
