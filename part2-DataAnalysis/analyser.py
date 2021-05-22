import pandas as pd
import sys

# Reading Data from command line
data = sys.argv[1]

# Storing data in a dataframe
marklist = pd.read_csv(data)

# Creating a new column Total for analysing Overall Class Toppers
marklist['Total'] = marklist.iloc[:, 1:7].sum(axis=1)

# Finding and printing Toppers of each subject
for subject in marklist[ marklist.columns.drop(['Name', 'Total'])]:
    # pass
    print("Topper in %s is %s" %(subject, marklist[ (marklist[subject] == marklist[subject].max())].iloc[0]['Name'] ) )

# Printing Class Toppers based on their Total Marks from all Subjects
toppers = marklist.sort_values('Total', ascending=False).iloc[0:3]

print("\nBest Students in the class are %s, %s, %s" %(toppers.iloc[0]['Name'], toppers.iloc[1]['Name'], toppers.iloc[2]['Name']) )
