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

# Create a scatter plot of each player's Opponent Batting Average at each age
plt.scatter(df['age'], df['BAOpp'], alpha=0.5)

plt.xlabel('Age')
plt.ylabel('Opponent Batting Average')
plt.title('Opponent Batting Average by Age')
plt.show()