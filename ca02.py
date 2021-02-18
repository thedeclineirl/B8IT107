'''
DBS Higher Diploma in Data Analytics
B8IT107 - Data Visualization & Communications
CA2
Thomas Higgins - 10544739
Gerard Keaty - 10544675
Camila Kosma -  10338540
Created:    2021-02-13
Edited:     2021-02-15
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
import random

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# # create functions for data clean-up and column splitting 

def fix_postcode(column):
    # Postcodes are missing for Burlington vermont, 5401, so they need to be added manually
    if column == '':
        return '5401'
    else:
        # columns intially imported as floats, they were converted to string but now we need to get rid of the .0 at the end
        temp = column.split('.')
        return temp[0]

def get_year(column):
    date = column.split('/')
    return date[2]

def get_month(column):
    date = column.split('/')
    return date[1]

def get_dom(column):
    date = column.split('/')
    return date[0]

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# # Importing dataset and examining it

import_path = "datasets/train.csv"
export_path = "datasets/train_cleaned.csv"

dataset = pd.read_csv(import_path)
state_pop = pd.read_csv("datasets/state_pop.csv")
print(dataset.head())
print(dataset.shape)
print(dataset.info())
# print(dataset['Region'])
# print(sum(dataset['Sales']))
# print(sum(state_pop['population 2019']))

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# # cleaning the dataset, adding missing values and exporting a cleaned csv for use in tableau

# drop Row ID because we don't need it for the data analysis
dataset = dataset.drop(axis = 1, labels = 'Row ID')       
# convert Postal code to string
dataset['Postal Code'] = dataset['Postal Code'].astype(str) 
# add in missing postcodes
dataset['Postal Code'] = dataset['Postal Code'].apply(fix_postcode)
# # examine dataset for changes
# print(dataset.info())

# export dataset as is for analysis in Tableau
dataset.to_csv(export_path,index = False)

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# # adding extra columns for analysis in Python

# Create date columns based on order date
dataset['order_year'] = dataset['Order Date'].apply(get_year)
dataset['order_month'] = dataset['Order Date'].apply(get_month)
dataset['order_dom'] = dataset['Order Date'].apply(get_dom)
# # examine dataset for changes
# print(dataset.info())

# convert the new columns to numeric 
dataset['order_year'] = dataset['order_year'].apply(pd.to_numeric)
dataset['order_month'] = dataset['order_month'].apply(pd.to_numeric)
dataset['order_dom'] = dataset['order_dom'].apply(pd.to_numeric)

# drop columns we won't use
dataset = dataset.drop(axis = 1, labels = ['Order Date', 'Ship Date'])  

# # examine dataset for changes again
print(dataset.info())

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# create variable for iterating through the datset

regions = ['East','South','Central','West']
years = [2015,2016,2017,2018]
categories = ['Furniture','Office Supplies','Technology']
colours = ['red','green','blue','yellow','pink','orange','purple']

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# # Create Functions for drawing the plots

def sankey_total_sales_by_region(df):
    # Calculate sales 
    total_sales = sum(df['Sales'])
    south_sales = df.loc[dataset['Region'] == 'South', 'Sales'].sum() 
    east_sales = df.loc[dataset['Region'] == 'East', 'Sales'].sum()
    west_sales = df.loc[dataset['Region'] == 'West', 'Sales'].sum()
    central_sales = df.loc[dataset['Region'] == 'Central', 'Sales'].sum()
    # Plot Sankey 
    Sankey(
        flows=[south_sales, east_sales, west_sales, central_sales, -total_sales],
        labels=['South', 'East', 'West', 'Central', 'Total'],
        orientations=[0, 0, 1, -1, 0],
        # fill = False
           ).finish()
    plt.title("Total Sales by Region, in $1000")
    plt.show()

def sankey_total_sales_by_region_by_year_in_K(df,year):
    # Calculate sales
    total_sales = df.loc[df['order_year'] == year, 'Sales'].sum()
    south_sales = df.loc[((df['Region'] == 'South') & (df['order_year'] == year)), 'Sales'].sum() 
    east_sales = df.loc[((df['Region'] == 'East') & (df['order_year'] == year)), 'Sales'].sum()
    west_sales = df.loc[((df['Region'] == 'West') & (df['order_year'] == year)), 'Sales'].sum()
    central_sales = df.loc[((df['Region'] == 'Central') & (df['order_year'] == year)), 'Sales'].sum()

    # reduce to sales in thousands for cleaner plotting
    total_sales_K = int(total_sales/1000)
    south_sales_K = int(south_sales/1000)
    west_sales_K = int(west_sales/1000)
    east_sales_K = int(east_sales/1000)
    central_sales_K = int(central_sales/1000)
    # Sankey Diagram of sales by Region in Year
    Sankey(
        flows=[south_sales_K, east_sales_K, west_sales_K, central_sales_K, -total_sales_K],
        labels=['South', 'East', 'West', 'Central', 'Total'],
        orientations=[0, 0, 1, -1, 0]
           ).finish()
    plt.title(year+' :Total Sales by Region, in $1000')
    plt.show()

def sankey_total_sales_by_category_in_region_in_year(df,region,year,colour):
    total_sales = df.loc[((df['Region'] == region) & (df['order_year'] == year)), 'Sales'].sum()
    f_sales = df.loc[((df['Region'] == region) & (df['order_year'] == year)& (df['Category'] == 'Furniture')), 'Sales'].sum() 
    o_sales = df.loc[((df['Region'] == region) & (df['order_year'] == year)& (df['Category'] == 'Office Supplies')), 'Sales'].sum() 
    t_sales = df.loc[((df['Region'] == region) & (df['order_year'] == year)& (df['Category'] == 'Technology')), 'Sales'].sum() 
    
    # Sankey Diagram of sales by category in Region in Year
    Sankey(
        flows=[f_sales, o_sales, t_sales, -total_sales], # input values & output value with leading minus
        labels=['Furniture', 'Office Supplies', 'Technology', 'Total'], # labels for all values
        unit = '$', # units of I/O
        orientations=[-1, 1, 0, 0], 
        facecolor = colour, 
        head_angle = 120,
        scale=0.25, 
        rotation=-90, # diagram rotation
           ).finish()
    plt.title(str(year)+' :Total Sales by Category in '+region)
    plt.show()


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# # Running plotting Functions
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

# # Sankey of total sales by region
# sankey_total_sales_by_region(dataset)

# # Sankey of total sales by region & year in Thousands
# for y in years:
    # sankey_total_sales_by_region_by_year_in_K(dataset,y)

# # sankey of category in regions & years, with in random colours
# for r in regions:
#       for y in years:
#           colour = random.choice(colours)
#           sankey_total_sales_by_category_in_region_in_year(dataset,r,y,colour)

