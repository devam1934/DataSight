import pandas as pd

def classify_column(series:pd.Series)->str:
    non_null = series.dropna()

    if non_null.empty:
        return "unknown"
    
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    
    converted_datetime = pd.to_datetime(non_null, errors="coerce")
    if converted_datetime.notna().sum() / len(non_null) > 0.8:
        return "datetime"

    unique_ratio = non_null.nunique() / len(non_null)

    if series.dtype == "object":
        avg_len = non_null.astype(str).str.len().mean()

        if unique_ratio < 0.5 and avg_len < 50:
            return "categorical"

        return "text"

    return "unknown"

def build_profile(df:pd.DataFrame):
    profile = []

    for column in df.columns:
        series = df[column]

        profile.append({
            "column_name": column,
            "dtype": str(series.dtype),
            "semantic_type": classify_column(series),
            "missing_values": int(series.isna().sum()),
            "unique_values": int(series.nunique(dropna=True)),
            "sample_values": series.dropna().astype(str).head(5).tolist()
        })

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "profile": profile
    }
