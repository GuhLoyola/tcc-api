import pandas as pd
from ml.model.model_manager_loader import dataset_path, original_dataset_path

input_path = original_dataset_path
output_path = dataset_path

df = pd.read_csv(input_path)

if "url" not in df.columns:
    raise ValueError("O dataset deve conter uma coluna chamada 'url'.")

def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        return ""

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not url.endswith("/"):
        url += "/"

    return url

df["url"] = df["url"].apply(normalize_url)

df.to_csv(output_path, index=False)

print(f"✅ Dataset normalizado salvo")
print(df.head())
