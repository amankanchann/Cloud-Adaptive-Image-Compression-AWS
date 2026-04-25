import streamlit as st
import time
from datetime import datetime

from aws_clients import s3
from config import INPUT_BUCKET

def render_upload_section():
    st.markdown("## Upload Images")

    uploaded_files = st.file_uploader(
        "Choose image files",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    uploaded_keys = []

    if uploaded_files:
        st.write("Selected files:")
        for file in uploaded_files:
            st.write("-", file.name)

        if st.button("Upload and Process All"):
            uploaded_count = 0
            failed_files = []

            for uploaded_file in uploaded_files:
                try:
                    unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S_%f')}_{uploaded_file.name}"

                    s3.put_object(
                        Bucket=INPUT_BUCKET,
                        Key=unique_name,
                        Body=uploaded_file.getvalue(),
                        ContentType=uploaded_file.type
                    )

                    uploaded_keys.append(unique_name)
                    uploaded_count += 1

                except Exception as e:
                    failed_files.append(f"{uploaded_file.name}: {str(e)}")

            st.success(f"{uploaded_count} file(s) uploaded successfully.")
            time.sleep(4)
            st.info("Processing started. Scroll down or refresh to see updated results.")

            if failed_files:
                st.error("Some files failed:")
                for err in failed_files:
                    st.write(err)

    return uploaded_keys