import pandas as pd
import boto3
import os
from datetime import datetime

# AWS Configuration
AWS_BUCKET_NAME = "leverage-donor-data-staging"
S3_CLIENT = boto3.client('s3')

def clean_donor_data(file_path: str) -> pd.DataFrame:
    """Ingests and cleans messy campaign donor data."""
    print("Ingesting raw donor data...")
    df = pd.read_csv(file_path)

    # 1. Standardize text
    df['donor_name'] = df['donor_name'].str.strip().str.title()
    df['state'] = df['state'].str.strip().str.upper()

    # 2. Fix date formatting
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # 3. Filter invalid data (e.g., negative amounts / refunds)
    df = df[df['amount'] > 0]
    
    # 4. Flag missing contact info for the Client Services team
    df['needs_enrichment'] = df['email'].isna()

    return df

def run_qa_validation(df: pd.DataFrame):
    """Acts as the final QA check before shipping to downstream systems."""
    print("Running QA Validation checks...")
    
    # Assert no negative donations slipped through
    assert (df['amount'] > 0).all(), "QA Failed: Negative donation amounts detected."
    
    # Assert standard state code length
    assert (df['state'].str.len() == 2).all(), "QA Failed: Invalid state codes detected."
    
    print("✅ All QA checks passed.")

def upload_to_aws(df: pd.DataFrame):
    """Mocks the upload of clean data to AWS S3."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"clean_donors_{timestamp}.csv"
    
    # Save locally first
    df.to_csv(file_name, index=False)
    
    print(f"Uploading {file_name} to AWS S3 bucket: {AWS_BUCKET_NAME}...")
    # In a production environment, this triggers the Boto3 upload:
    # S3_CLIENT.upload_file(file_name, AWS_BUCKET_NAME, file_name)
    print("✅ Upload complete.")

if __name__ == "__main__":
    # Execute the pipeline
    clean_df = clean_donor_data("messy_donors.csv")
    run_qa_validation(clean_df)
    upload_to_aws(clean_df)
