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
(Add screenshots here)