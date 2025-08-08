import pandas as pd
import re

# Load the CSV file (make sure 'outputs_20.csv' is in the same folder as this script)
df = pd.read_csv('outputs_20.csv')

# Ensure the column has a consistent name
df.columns = ['Output']

# Define keyword-based category matching
category_keywords = {
    'Fault detection': [r'\bfault detection\b', r'\bdetection\b', r'\berror detection\b'],
    'Fault prediction': [r'\bfault prediction\b', r'\bfailure prediction\b', r'\bprediction\b', r'\bforecasting\b'],
    'Fault diagnosis': [r'\bfault diagnosis\b', r'\bdiagnosis\b', r'\bdiagnostic\b'],
    'Remaining Useful Life': [r'\bremaining useful life\b', r'\brul\b', r'\btime to failure\b'],
    'Root cause analysis': [r'\broot cause\b', r'\blocalization\b'],
    'Predictive maintenance': [r'\bpredictive maintenance\b', r'\bmaintenance prediction\b', r'\bprognostics\b']
}

# Function to map output to categories
def map_to_category(output):
    output_lower = str(output).lower()
    for category, patterns in category_keywords.items():
        for pattern in patterns:
            if re.search(pattern, output_lower):
                return category
    return 'Other'

# Apply categorization
df['Category'] = df['Output'].apply(map_to_category)

# Save to new CSV
df.to_csv('outputs_20_categorized.csv', index=False)

print("Categorization complete! Results saved to 'outputs_20_categorized.csv'.")
