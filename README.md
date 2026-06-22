# Leverage Data Engineering PoW: Donor Data Automation 🚀

A lightweight data engineering pipeline built to demonstrate the ingestion, cleaning, QA validation, and AWS staging of messy progressive campaign data. 

*Note: This pipeline was rapidly prototyped using GitHub Copilot, reflecting a pragmatic approach to AI-assisted engineering velocity.*

## The Workflow
1. **Ingestion & Transformation:** A Python script (`pandas`) takes a messy CSV of donor records, standardizes text, unifies date formats, and flags missing emails for downstream enrichment.
2. **QA Validation:** Built-in assertion checks act as a strict quality gate, ensuring no negative refund amounts or malformed state codes pass through to the database.
3. **Cloud Infrastructure:** Leverages `boto3` to automate the secure staging of the cleaned data payload into an **AWS S3** bucket. 

## Tech Stack
* Python (Pandas)
* AWS (Boto3 / S3)
* GitHub Copilot (AI-Assisted Development)
