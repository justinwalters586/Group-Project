import pandas as pd
import matplotlib.pyplot as plt

# Load the data
batting_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/Batting.xlsx')
people_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/People.xlsx')

# Join the data on the playerID
df = pd.merge(batting_df, people_df, on='playerID')

# Calculate the players' birthdates
df['age'] = df['yearID'] - df['birthYear']

# Filter out records where 'AB' is 0 and 'exact_age' is not within a reasonable range
df = df[(df['AB'] >= 100) & (df['age'] >= 20) & (df['age'] <= 40)]

# Calculate the batting average for each player at each age
df['batting_average'] = df['H'] / df['AB']

# Create a scatter plot of each player's batting average at each age
plt.scatter(df['age'], df['batting_average'], alpha=0.5)

plt.xlabel('Age')
plt.ylabel('Batting Average')
plt.title('Batting Average by Age')
plt.show()