

import pandas as pd
import numpy as np
import unidecode
# Set seed for reproducibility
np.random.seed(42)

# Define the number of rows and columns
num_rows = 3
num_columns = 4

# Create a DataFrame with random values
data = np.random.rand(num_rows, num_columns)

# Create column names
columns = [f"Column_{i+1}" for i in range(num_columns)]

# Create the DataFrame
df = pd.DataFrame(data, columns=columns)

# Display the DataFrame
print(df)
print(df["Column_4"][1])
df["Column_4"][1] = 3
print(df)
word = ["Column_1","Column_2","Column_3"]
for i in range(3):
	#word_split = doc_files[i].lower().split()
	for w in word:
		df[w][i+1] = 1
	
print(df)
#
doc = " The new ways of the dr richard richard jones in amnesia the dark descent youtube"
stop_words = ["the","in","of"]
split = doc.lower().split()
print(list(set(split)))
input('wait')
print(split)
for w in list(set(split) - set(stop_words)):
	print(w)
print(unidecode.unidecode('the new 80s was of three\'s DATA scientits 3'))
