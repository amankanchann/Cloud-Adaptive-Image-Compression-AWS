import streamlit as st
from PIL import Image
import io
from streamlit_image_comparison import image_comparison

from aws_clients import table, s3
from config import OUTPUT_BUCKET, INPUT_BUCKET
from helpers import prepare_dashboard_dataframe, calculate_metrics, get_s3_image_bytes


def resize_for_display(image_file, size=(1600, 850)):
    image = Image.open(image_file)
    image = image.resize(size)
    return image


def render_dashboard():
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        st.warning("No metadata records found in DynamoDB.")
        return

    df = prepare_dashboard_dataframe(items)

    if df.empty:
        st.warning("No valid records to display.")
        return

    metrics = calculate_metrics(df)

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Files Processed", metrics["total_files"])
    col2.metric("Total Original Size (KB)", metrics["total_original"])
    col3.metric("Total Compressed Size (KB)", metrics["total_compressed"])
    col4.metric("Total Storage Saved (KB)", metrics["total_saved"])

    st.markdown("### Compression Analysis")
    col5, col6 = st.columns(2)
    col5.metric("Average Compression Ratio (%)", metrics["avg_ratio"])
    col6.metric("Successful Compressions", metrics["success_count"])

    # Metadata table
    st.markdown("### Metadata Records")
    st.dataframe(df, use_container_width=True)

    # Status table
    st.markdown("### Status Distribution")
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    st.table(status_counts)

    # Preview section
    st.markdown("### Original vs Compressed Preview")

    if "filename" in df.columns:
        selected_file = st.selectbox("Select image to preview", df["filename"].tolist())

        selected_row = df[df["filename"] == selected_file].iloc[0]

        status = str(selected_row.get("status", ""))
        original_size = selected_row.get("original_size_kb", "NA")
        compressed_size = selected_row.get("compressed_size_kb", "NA")
        chosen_quality = selected_row.get("chosen_quality", "NA")
        compression_gain = selected_row.get("compression_gain", "NA")

        st.markdown(
            f"**Original Size:** {original_size} KB  |  "
            f"**Compressed Size:** {compressed_size} KB  |  "
            f"**Chosen Quality:** {chosen_quality}  |  "
            f"**Gain:** {compression_gain}%"
        )

        # Slider comparison
        if status == "Compressed":
            try:
                original_img_bytes = get_s3_image_bytes(s3, INPUT_BUCKET, selected_file)
                compressed_img_bytes = get_s3_image_bytes(s3, OUTPUT_BUCKET, selected_file)

                original_img = resize_for_display(original_img_bytes)
                compressed_img = resize_for_display(compressed_img_bytes)

                image_comparison(
                    img1=original_img,
                    img2=compressed_img,
                    label1="Original",
                    label2="Compressed",
                    width=500,
                    starting_position=50,
                    show_labels=True,
                    make_responsive=True,
                    in_memory=True,
                )

            except Exception as e:
                st.error(f"Unable to load comparison images: {e}")
        else:
            st.info(f"No compressed output available for this file. Status: {status}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Original Image**")
                try:
                    original_img = get_s3_image_bytes(s3, INPUT_BUCKET, selected_file)
                    original_img = resize_for_display(original_img)
                    st.image(original_img)
                except Exception as e:
                    st.error(f"Original image not found: {e}")

            with col2:
                st.markdown("**Compressed Image**")
                st.info("Not available")

        st.info(
            "The slider provides a visual comparison. Size reduction and compression gain show the measurable optimization result."
        )

        # Details
        st.markdown("### Processing Details")

        details_cols = [
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

        for col in details_cols:
            if col in selected_row:
                st.write(f"**{col}**: {selected_row[col]}")