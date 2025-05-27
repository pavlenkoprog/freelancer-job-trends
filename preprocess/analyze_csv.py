import pandas as pd


def analyze_csv_for_prompt(csv_path, max_unique=10):
    df = pd.read_csv(csv_path)
    metadata_lines = []

    for col in df.columns:
        dtype = str(df[col].dtype)
        uniques = df[col].dropna().unique()
        n_unique = len(uniques)

        # Пример значений
        if n_unique <= max_unique:
            example_values = ', '.join(map(repr, uniques))
        else:
            sample_values = ', '.join(map(repr, uniques[:max_unique]))
            example_values = f"{sample_values}, ... (+{n_unique - max_unique} more)"

        metadata_lines.append(
            f"- `{col}` ({dtype}, {n_unique} unique): {example_values}"
        )

    return metadata_lines


# Пример использования
if __name__ == "__main__":
    csv_path = "../data/freelancer_earnings_bd.csv"  # укажите путь к вашему файлу
    prompt_metadata = analyze_csv_for_prompt(csv_path)
    print(prompt_metadata)

# Колонки с категориями:
# - `Job_Category` (object, 8 unique): 'Web Development', 'App Development', 'Data Entry', 'Digital Marketing', 'Customer Support', 'Content Writing', 'Graphic Design', 'SEO'
# - `Platform` (object, 5 unique): 'Fiverr', 'PeoplePerHour', 'Upwork', 'Toptal', 'Freelancer'
# - `Experience_Level` (object, 3 unique): 'Beginner', 'Intermediate', 'Expert'
# - `Client_Region` (object, 7 unique): 'Asia', 'Australia', 'UK', 'Europe', 'USA', 'Middle East', 'Canada'
# - `Payment_Method` (object, 4 unique): 'Mobile Banking', 'Crypto', 'Bank Transfer', 'PayPal'
# - `Project_Type` (object, 2 unique): 'Fixed', 'Hourly'
