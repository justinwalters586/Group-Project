import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
pitching_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/Pitching.xlsx')
people_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/People.xlsx')

# Join the data on the playerID
df = pd.merge(pitching_df, people_df, on='playerID')

# Calculate the players' birthdates
df['age'] = df['yearID'] - df['birthYear']

# Filter out records where 'IPouts' is less than 150 and 'exact_age' is not within a reasonable range
df = df[(df['IPouts'] >=150) & (df['age'] >= 20) & (df['age'] <= 40)]

# Calculate the 1st percentile of ERA for each age
df['top_1_percent'] = df.groupby('age')['BAOpp'].transform(lambda x: x.quantile(0.0005))

# Filter out the rows that are not in the top 1% of ERA for each age
top_1_percent_df = df[df['BAOpp'] <= df['top_1_percent']]

# Fit a quadratic curve (degree=2) to these points
z = np.polyfit(top_1_percent_df['age'], top_1_percent_df['BAOpp'], 2)
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
plt.scatter(df['age'], df['BAOpp'])

# Plot the trendline using the sorted DataFrame
plt.plot(top_1_percent_df['age'], p(top_1_percent_df['age']), "r--")

plt.xlabel('Age')
plt.ylabel('Opponent Batting Average')
plt.title('Opponent Batting Average by Age')
plt.show()