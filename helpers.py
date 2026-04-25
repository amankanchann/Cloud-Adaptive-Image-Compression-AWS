import pandas as pd
from io import BytesIO

def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        "original_size_kb",
        "compressed_size_kb",
        "compression_ratio",
        "compression_gain"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def prepare_dashboard_dataframe(items):
    if not items:
        return pd.DataFrame()

    df = pd.DataFrame(items)
    df = convert_numeric_columns(df)

    preferred_columns = [
        "filename",
        "format",
        "original_size_kb",
        "compressed_size_kb",
        "compression_ratio",
        "chosen_quality",
        "compression_gain",
        "decision_taken",
        "status",
        "upload_time",
    ]

    available_columns = [col for col in preferred_columns if col in df.columns]
    return df[available_columns]

def calculate_metrics(df: pd.DataFrame):
    total_files = len(df)
    total_original = df["original_size_kb"].sum() if "original_size_kb" in df.columns else 0
    total_compressed = df["compressed_size_kb"].sum() if "compressed_size_kb" in df.columns else 0
    total_saved = total_original - total_compressed
    avg_ratio = df["compression_ratio"].mean() if "compression_ratio" in df.columns else 0

    status_counts = df["status"].value_counts().to_dict() if "status" in df.columns else {}
    success_count = status_counts.get("Compressed", 0) + status_counts.get("Success", 0)

    return {
        "total_files": total_files,
        "total_original": round(total_original, 2),
        "total_compressed": round(total_compressed, 2),
        "total_saved": round(total_saved, 2),
        "avg_ratio": round(avg_ratio, 2) if pd.notna(avg_ratio) else 0,
        "success_count": success_count,
        "status_counts": status_counts
    }

def get_s3_image_bytes(s3_client, bucket_name: str, key: str):
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    return BytesIO(response["Body"].read())