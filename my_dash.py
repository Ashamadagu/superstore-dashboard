import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('superstore_data.csv')

# Set the title
st.set_page_config(page_title="Superstore Dashboard", page_icon=":clipboard:", layout="wide")
st.title("Superstore Dashboard")

# Display the first few rows of the dataset
st.subheader('First few rows of the dataset')
st.write(df.head())

# Display summary statistics for the dataset
st.subheader('Summary statistics')
st.write(df.describe())

# Display a list of columns in the dataset
st.subheader('List of columns')
st.write(list(df.columns))

# Set the title
st.title('Superstore Data')

# Display the question
st.header('What product sold most and why we think it sold most')

# Select the relevant columns
products_df = df.loc[:, ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']]

# Drop missing values and convert to float
products_df = products_df.dropna().astype(float)

# Display the summary statistics
st.subheader('Summary statistics for the relevant columns')
st.write(products_df.describe())

# Calculate the total amount of each product sold
total_sales = products_df.sum()

# Determine which product sold the most
product_sold_most = total_sales.idxmax()

# Display the product that sold the most
st.subheader('Product that sold the most')
st.write(product_sold_most)

# Display possible reasons why the product sold the most
st.subheader('Possible reasons why this product sold the most')
if product_sold_most == 'MntWines':
	st.write('Wine is a popular and widely consumed beverage, with a long history of cultural significance and social appeal.')
elif product_sold_most == 'MntFruits':
	st.write('Fruits are a healthy and nutritious food that are recommended as part of a balanced diet.')
elif product_sold_most == 'MntMeatProducts':
	st.write('Meat is a rich source of protein and other essential nutrients, and is a staple in many diets around the world.')
elif product_sold_most == 'MntFishProducts':
	st.write('Fish is a lean protein source that is rich in omega-3 fatty acids and other important nutrients, and is recommended as part of a healthy diet.')
elif product_sold_most == 'MntSweetProducts':
	st.write('Sweets are a popular treat that many people enjoy as a way to indulge their sweet tooth or reward themselves for good behavior.')
elif product_sold_most == 'MntGoldProds':
	st.write('Gold products may be purchased as luxury items or as a form of investment, and may hold both aesthetic and monetary value.')


# Calculate the total amount earned from the product that sold the most
amount_earned = products_df[product_sold_most].sum()

# Display the total amount earned from the product that sold the most
st.subheader('Total amount earned from the product that sold the most')
st.write('${:,.2f}'.format(amount_earned))


# Convert the 'Dt_Customer' column to datetime format
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])

# Group purchases by date and calculate the total purchases made on each date
daily_purchases = df.groupby('Dt_Customer').sum()[['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']]
daily_purchases['TotalPurchases'] = daily_purchases.sum(axis=1)

# Display a line chart of the total purchases made each day
st.subheader('Total Purchases by Day')
st.line_chart(daily_purchases['TotalPurchases'])

# Find the day with the highest total purchases and display the result
max_purchase_day = daily_purchases['TotalPurchases'].idxmax().strftime('%B %d, %Y')
st.subheader('Day with the highest total purchases')
st.write(max_purchase_day)

# Define function to find the product that sold the most
def product_sold_most(dataframe):
	products_df = dataframe.loc[:, ['MntWines',
									 'MntFruits',
									 'MntMeatProducts',
									 'MntFishProducts',
									 'MntSweetProducts',
									 'MntGoldProds']]
	products_df = products_df.dropna()
	products_df = products_df.astype(float)
	product_sold_most = products_df.sum().idxmax()
	return product_sold_most

# Define function to find the amount earned from the product that sold most
def amount_earned(dataframe, product_name):
	amount_earned = dataframe[product_name].sum()
	return amount_earned

# Define function to find the time to display advertisements to maximize buying of products
def time_to_display_ads(dataframe):
	purchase_df = dataframe.loc[:, ['NumDealsPurchases',
									'NumWebPurchases',
									'NumCatalogPurchases',
									'NumStorePurchases']]
	sum_ = purchase_df.sum(axis=1)
	purchase_df['total_purchase'] = sum_
	formated_date = pd.to_datetime(df['Dt_Customer']).astype('datetime64[ns]')
	purchase_df['formated_date'] = formated_date
	total_g_date = purchase_df.loc[:, ['formated_date', 'total_purchase']]
	total_date_grouped = total_g_date.groupby('formated_date')
	totals = total_date_grouped.sum()
	maxValues = totals.loc[totals['total_purchase'].idxmax()]
	return maxValues.name.date()

# Define function to find the product with the highest tax amount and freight charges
def highest_tax_amount_and_freight_charges(dataframe):
	salesOrder = pd.read_excel('DataSet_SalesOrders.xlsx')
	highestTaxAmount = salesOrder.loc[salesOrder['TaxAmt'].idxmax()]['ProdID']
	highestForeignCharges = salesOrder.loc[salesOrder['Freight'].idxmax()]['ProdID']
	return highestTaxAmount, highestForeignCharges

def products_bought_together(df):
	df = pd.read_excel('DataSet_SalesOrders.xlsx')
	order_ids = df['ProdID'].unique()
	product_pairs = {}
	for order_id in order_ids:
		order_products = df.loc[df['ProdID'] == order_id, 'ProdID'].tolist()
		
		# Sort the list of product IDs
		order_products.sort()
		
		# Loop through each pair of products in the current order
		for i in range(len(order_products) - 1):
			for j in range(i + 1, len(order_products)):
				# Combine the two product IDs into a tuple
				pair = (order_products[i], order_products[j])
				
				# If the pair is already in the dictionary, increment the count
				if pair in product_pairs:
					product_pairs[pair] += 1
				# Otherwise, add the pair to the dictionary with a count of 1
				else:
					product_pairs[pair] = 1
	
	# Get the pair with the highest frequency
	most_common_pair = max(product_pairs, key=product_pairs.get)
	
	# Return the two product IDs in the most common pair
	return most_common_pair

def total_revenue_and_profit():
	salesOrder = None
	# Calculate total revenue and profit
	df = pd.read_excel('DataSet_SalesOrders.xlsx')
	revenue = df['SubTotal'].sum()
	cost = df['TaxAmt'].sum() + df['Freight'].sum()
	profit = revenue - cost
	
	# Filter data by sales order
	if salesOrder:
		df = df[df['SalesOrderID'].isin(salesOrder)]
		revenue = df['SubTotal'].sum()
		cost = df['TaxAmt'].sum() + df['Freight'].sum()
		profit = revenue - cost
	
	return revenue, profit

def customers_with_highest_number_of_purchases():
	df = pd.read_excel('DataSet_SalesOrders.xlsx')
	
	customers = df.groupby('CustID').size().sort_values(ascending=False)
	top_customers = list(customers.index[:5])
	return top_customers



def main():
  
	# Section 1: Product that sold most and amount earned
	st.header("Product that sold most and amount earned")
	product_name = product_sold_most(df)
	amount = amount_earned(df, product_name)
	st.write(f"1. The product that sold most is {product_name}")
	st.write(f"2. The amount earned from the product that sold most is {amount:.2f}")

	# Section 2: Time to display advertisements to maximize buying of products
	st.header("Time to display advertisements to maximize buying of products")
	date = time_to_display_ads(df)
	st.write(f"3. The best time to display advertisements to maximize buying of products is {date}")

	# Section 3: Product with the highest tax amount and freight charges
	st.header("Product with the highest tax amount and freight charges")
	highest_tax, highest_freight = highest_tax_amount_and_freight_charges(df)
	st.write(f"4. The product with the highest tax amount is {highest_tax}")
	st.write(f"   The product with the highest freight charges is {highest_freight}")
	
	# Section 4: Products that are usually bought together
	st.header("Products that are usually bought together")
	product1, product2 = products_bought_together(df)
	st.write(f"5. The products that are usually bought together are {product1} and {product2}")
	
	# Section 5: Total revenue and profit
	st.header("Total revenue and profit")
	revenue, profit = total_revenue_and_profit()
	st.write(f"6. The total revenue is {revenue:.2f}")
	st.write(f"   The total profit is {profit:.2f}")
	
	# Section 6: Customers with the highest number of purchases
	st.header("Customers with the highest number of purchases")
	top_customers = customers_with_highest_number_of_purchases()
	st.write(f"7. The top customers with the highest number of purchases are Customers with ID:")
	for i, customer in enumerate(top_customers):
		st.write(f"   {i+1}. {customer}")

if __name__ == '__main__':
	main()