# Cloud-Based Adaptive Image Compression System (AWS)

## Overview
This project implements a serverless image compression system using AWS. It automatically compresses uploaded images to achieve approximately 50% size reduction while maintaining acceptable visual quality.

## Architecture
User → Streamlit UI → S3 Input Bucket → Lambda → S3 Output Bucket + DynamoDB → Dashboard

## Features
- Target-based compression (~50% reduction)
- Decision-based logic (skip small / low-gain images)
- Batch image upload
- Metadata tracking (size, gain, quality, status)
- Interactive dashboard with analytics
- Before/after image comparison slider

## AWS Services Used
- Amazon S3 (storage)
- AWS Lambda (processing)
- DynamoDB (metadata)
- IAM (permissions)
- CloudWatch (logging)

## Results
- Large images: ~50% reduction
- Medium images: ~40–60% reduction
- Small images: skipped

## Note
This project was deployed using Streamlit Cloud and AWS.  
Backend services may be disabled to avoid unnecessary cloud costs.

## Screenshots
<img width="1845" height="772" alt="Screenshot 2026-04-25 224830" src="https://github.com/user-attachments/assets/9249c0d2-d923-4270-b8bd-2d4beb4878e6" />
<img width="1737" height="650" alt="Screenshot 2026-04-25 224719" src="https://github.com/user-attachments/assets/7f08dd1f-9973-49b8-9471-cbb06a08b489" />
<img width="456" height="533" alt="Screenshot 2026-04-25 224728" src="https://github.com/user-attachments/assets/c28b4d53-5b66-4a83-98e3-9296b7089f79" />
