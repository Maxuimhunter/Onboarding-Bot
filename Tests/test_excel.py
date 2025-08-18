import pandas as pd
import os

print("Testing Excel file creation...")
test_file = "test_excel.xlsx"
print(f"Creating {test_file} in: {os.getcwd()}")

# Create a simple DataFrame
data = {
    'Name': ['Test User'],
    'Email': ['test@example.com']
}

df = pd.DataFrame(data)

# Try to save to Excel
try:
    df.to_excel(test_file, index=False)
    if os.path.exists(test_file):
        print(f"SUCCESS: {test_file} created successfully!")
        print(f"File size: {os.path.getsize(test_file)} bytes")
    else:
        print("ERROR: File was not created!")
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
