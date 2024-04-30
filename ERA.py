import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
pitching_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/Pitching.xlsx')
people_df = pd.read_excel('C:/Users/WaltersJ07/Downloads/People.xlsx')

# Join the data on the playerID
df = pd.merge(pitching_df, people_df, on='playerID')

# Calculate the players' ages
df['age'] = df['yearID'] - df['birthYear']

# Filter out records where 'ERA' is 0 and 'age' is not within a reasonable range
df = df[(df['ERA'] != 0) & (df['age'] >= 20) & (df['age'] <= 40) & (df['IPouts'] > 150)]

# Scatter plot of each player's ERA at their specific age
plt.scatter(df['age'], df['ERA'], alpha=0.5)

# Show the plot with labels
plt.xlabel('Age')
plt.ylabel('ERA')
plt.title('ERA by Age')
plt.grid(True)
plt.show()