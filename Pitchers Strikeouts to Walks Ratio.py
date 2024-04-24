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

# Filter out records where 'BB' is 0 and 'exact_age' is not within a reasonable range
df = df[(df['BB'] !=0) & (df['SO'] !=0) & (df['IPouts'] >=150) & (df['age'] >= 20) & (df['age'] <= 40)]

# Calculate the Strikeouts-Walks Ratio for each player at each age
# Add a small constant to avoid division by zero
df['strikeouts_walks_ratio'] = df['SO'] / (df['BB'] + np.finfo(float).eps)

# Create a scatter plot of each player's Strikeouts-Walks Ratio at each age
plt.scatter(df['age'], df['strikeouts_walks_ratio'], alpha=0.5)

plt.xlabel('Age')
plt.ylabel('Strikeouts-Walks Ratio')
plt.title('Strikeouts-Walks Ratio by Age')
plt.show()