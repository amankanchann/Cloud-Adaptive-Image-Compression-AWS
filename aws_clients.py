import boto3
import streamlit as st
from config import AWS_REGION, DYNAMODB_TABLE

s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=AWS_REGION,
)

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=AWS_REGION,
)

table = dynamodb.Table(DYNAMODB_TABLE)