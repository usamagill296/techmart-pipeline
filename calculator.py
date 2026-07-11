import pandas as pd

data = {
    "name": ["Usama", "Anna", "John", "Sara"],
    "salary": [55000, 48000, 62000, 51000],
    "city": ["Berlin", "Munich", "Hamburg", "Berlin"]
}

df = pd.DataFrame(data)

print("All employees:")
print(df)

print("\nOnly Berlin employees:")
berlin_employees = df[df["city"] == "Berlin"]
print(berlin_employees)

print("\nOnly employees with salary above 50000:")
high_salary = df[df["salary"] > 50000]
print(high_salary)

print(f"Average salary: {df['salary'].mean()}")
print(f"Total salary:   {df['salary'].sum()}")
print(f"Highest salary: {df['salary'].max()}")
print(f"Lowest salary:  {df['salary'].min()}")
print(f"Total employees:{df['salary'].count()}")