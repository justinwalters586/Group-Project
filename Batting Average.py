import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
batting_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/Batting.xlsx')
people_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/People.xlsx')

# Join the data on the playerID
df = pd.merge(batting_df, people_df, on='playerID')

# Calculate the players' ages
df['age'] = df['yearID'] - df['birthYear']

# Filter out records where 'AB' is less than 100 and 'age' is not within a reasonable range
df = df[(df['AB'] >= 100) & (df['age'] >= 20) & (df['age'] <= 40)]

# Calculate the batting average for each player at each age
df['batting_average'] = df['H'] / df['AB']

# Calculate the 99th percentile of batting average for each age
df['top_1_percent'] = df.groupby('age')['batting_average'].transform(lambda x: x.quantile(0.9995))

# Filter out the rows that are not in the top 1% of batting average for each age
top_1_percent_df = df[df['batting_average'] >= df['top_1_percent']]

# Fit a quadratic curve (degree=2) to these points
z = np.polyfit(top_1_percent_df['age'], top_1_percent_df['batting_average'], 2)
p = np.poly1d(z)

# Calculate the derivative of the polynomial
p_derivative = p.deriv()

# Find the roots of the derivative (i.e., the values of x where the slope is 0)
roots = np.roots(p_derivative)

# Filter out the roots that are outside the range of ages
peak_ages = roots[(roots >= df['age'].min()) & (roots <= df['age'].max())]

# Print out the peak performance ages
for age in peak_ages:
    print(f'Peak performance age: {age}')

# Sort top_1_percent_df by 'age'
top_1_percent_df = top_1_percent_df.sort_values('age')

# Create a scatter plot
plt.scatter(df['age'], df['batting_average'])

# Plot the trendline using the sorted DataFrame
plt.plot(top_1_percent_df['age'], p(top_1_percent_df['age']), "r--")

plt.xlabel('Age')
plt.ylabel('Batting Average')
plt.title('Batting Average by Age')
plt.show()