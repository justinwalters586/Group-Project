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

# Filter out records where 'AB' is less than 200 and 'age' is not within a reasonable range
df = df[(df['AB'] >= 100) & (df['age'] >= 20) & (df['age'] <= 40)]

# Group the data by age and playerID and sum up 'HR' for each player at each age
grouped_by_age_and_player = df.groupby(['age', 'playerID']).agg(
    total_home_runs=('HR', 'sum')
)

# Reset index to make 'age' and 'playerID' as columns again
grouped_by_age_and_player.reset_index(inplace=True)

# Calculate the 99th percentile of home runs for each age
grouped_by_age_and_player['top_1_percent'] = grouped_by_age_and_player.groupby('age')['total_home_runs'].transform(lambda x: x.quantile(0.99))

# Filter out the rows that are not in the top 1% of home run hitters for each age
top_1_percent_df = grouped_by_age_and_player[grouped_by_age_and_player['total_home_runs'] >= grouped_by_age_and_player['top_1_percent']]

# Fit a quadratic curve (degree=2) to these points
z = np.polyfit(top_1_percent_df['age'], top_1_percent_df['total_home_runs'], 2)
p = np.poly1d(z)

# Calculate the derivative of the polynomial
p_derivative = p.deriv()

# Find the roots of the derivative (i.e., the values of x where the slope is 0)
roots = np.roots(p_derivative)

# Filter out the roots that are outside the range of ages
peak_ages = roots[(roots >= grouped_by_age_and_player['age'].min()) & (roots <= grouped_by_age_and_player['age'].max())]

# Print out the peak performance ages
for age in peak_ages:
    print(f'Peak performance age: {age}')

# Create a scatter plot
plt.scatter(grouped_by_age_and_player['age'], grouped_by_age_and_player['total_home_runs'])
plt.plot(top_1_percent_df['age'], p(top_1_percent_df['age']), "r--")
plt.xlabel('Age')
plt.ylabel('Home Runs')
plt.title('Home Runs by Age')
plt.show()