import streamlit as st
from PIL import Image
import os
import shutil

import openpyxl
#LinkedIn Profile
with st.sidebar:
    st.write("### Abhishek Kumawat :sunglasses:")
    st.components.v1.html(
    """
    <div style="display: flex; justify-content: center;">
        <a href="https://www.linkedin.com/in/abhishek-kumawat-iitd/" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="35">
        </a>
    </div>
    """
    )
def overlay_logo(image, logo, position="bottom-right", padding=10):
    """
    Overlays the logo onto the image at the specified position with padding.
    
    Parameters:
    - image: The base image (PIL Image object).
    - logo: The logo image (PIL Image object).
    - position: The position of the logo ("top-left", "top-right", "bottom-left", "bottom-right").
    - padding: Padding around the logo in pixels.

    Returns:
    - A new PIL Image object with the logo overlaid.
    """
    image = image.convert("RGBA")
    logo = logo.convert("RGBA")

    # Resize logo to a smaller size relative to the image
    logo_width = image.width // 8
    logo_ratio = logo_width / logo.width
    logo_height = int(logo.height * logo_ratio)
    logo = logo.resize((logo_width, logo_height))

    # Determine position
    if position == "bottom-right":
        x = image.width - logo.width - padding
        y = image.height - logo.height - padding
    elif position == "bottom-left":
        x = padding
        y = image.height - logo.height - padding
    elif position == "top-right":
        x = image.width - logo.width - padding
        y = padding
    elif position == "top-left":
        x = padding
        y = padding
    else:
        raise ValueError("Invalid position. Choose from 'top-left', 'top-right', 'bottom-left', 'bottom-right'.")

    # Overlay logo
    image.paste(logo, (x, y), logo)
    return image

def main():
    st.title("Logo Overlay Tool")
    st.write("Upload multiple images and a logo to overlay it on them.")

    # Upload logo
    logo_file = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])

    # Upload images
    image_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # Choose position
    position = st.selectbox("Select Logo Position", ["top-left", "top-right", "bottom-left", "bottom-right"], index=3)

    # Add padding input
    padding = st.slider("Padding around Logo (pixels)", min_value=0, max_value=500, value=10)

    if logo_file and image_files:
        logo = Image.open(logo_file)

        # Create a directory to save processed images
        output_dir = "processed_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        st.write("### Processed Images")
        for image_file in image_files:
            image = Image.open(image_file)
            processed_image = overlay_logo(image, logo, position=position, padding=padding)

            # Convert to RGB if saving as JPEG
            processed_image = processed_image.convert("RGB")
            save_path = os.path.join(output_dir, image_file.name)
            processed_image.save(save_path)

            # Display processed image
            st.image(processed_image, caption=f"Processed: {image_file.name}", use_container_width=True)

        # Provide download link
        st.write("All images processed! You can download them as a zip file below.")

        # Create ZIP file using shutil
        zip_path = "processed_images.zip"
        shutil.make_archive("processed_images", "zip", output_dir)

        with open(zip_path, "rb") as zip_file:
            st.download_button(
                label="Download All Images",
                data=zip_file,
                file_name="processed_images.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
