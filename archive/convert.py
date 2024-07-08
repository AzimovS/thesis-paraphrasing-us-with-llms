import pandas as pd

# Assuming your dataset is stored in a CSV file named "dataset.csv"
dataset = pd.read_csv("from.csv")

# Create a new column 'text' by concatenating values from selected columns
dataset['prompt'] = "Paraphrase the following user story: " + dataset['User Story'] + ".\n"
dataset['prompt'] += "Based on the following metrics: "
for col in dataset.columns:
    if col.startswith('diff'):
        dataset['prompt'] += col + ": " + dataset[col].astype(str) + ","
dataset['response'] = dataset['Paraphrased User Story']

# Selecting the columns
selected_columns = ['prompt'] + [col for col in dataset.columns if col.startswith('diff.')]

# Creating a new DataFrame with selected columns
selected_data = dataset[['prompt', 'response']]
train_df = selected_data.sample(frac=0.9, random_state=42)
test_df = selected_data.drop(train_df.index)

train_df.to_json('train.jsonl', orient='records', lines=True)
test_df.to_json('test.jsonl', orient='records', lines=True)
