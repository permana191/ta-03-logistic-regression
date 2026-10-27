import pandas as pd

def check_data():
    print("Memuat dataset...")
    df = pd.read_csv('dataset/data.csv')

    print(f"Dimensi Data: {df.shape}")
    print(f"Total Nilai Kosong: {df.isnull().sum().sum()}")

    target_col = 'Bankrupt?'
    if target_col in df.columns:
        print("\nDistribusi Kelas Target:")
        print(df[target_col].value_counts(normalize=True) * 100)
    else:
        print("Kolom target tidak ditemukan.")

if __name__ == "__main__":
    check_data()