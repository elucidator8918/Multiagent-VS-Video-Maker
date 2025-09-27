import os
import uuid
import tempfile
import numpy as np
import streamlit as st
from moviepy import VideoFileClip, CompositeVideoClip

def green_to_red(frame):
    """
    Replace green dot pixels with red.
    """
    new_frame = frame.copy()

    # Define "green" range (tune if needed)
    lower = np.array([0, 180, 0])     # dark green lower bound
    upper = np.array([100, 255, 100]) # light green upper bound

    # Create mask where green pixels are found
    mask = ((frame[:,:,0] >= lower[0]) & (frame[:,:,0] <= upper[0]) &   # R channel
            (frame[:,:,1] >= lower[1]) & (frame[:,:,1] <= upper[1]) &   # G channel
            (frame[:,:,2] >= lower[2]) & (frame[:,:,2] <= upper[2]))    # B channel

    # Replace green with red
    new_frame[mask] = [255, 0, 0]

    return new_frame

st.title("🎥 Video Overlay with Green → Red Filter")

# Upload videos
video1_file = st.file_uploader("Upload first video (background)", type=["mp4", "mov", "avi"])
video2_file = st.file_uploader("Upload second video (with green dot)", type=["mp4", "mov", "avi"])

if video1_file and video2_file:
    if st.button("Process Videos"):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save uploads to temp files
            video1_path = os.path.join(tmpdir, f"{uuid.uuid4()}_video1.mp4")
            video2_path = os.path.join(tmpdir, f"{uuid.uuid4()}_video2.mp4")
            output_path = os.path.join(tmpdir, f"{uuid.uuid4()}_output.mp4")

            with open(video1_path, "wb") as f:
                f.write(video1_file.read())
            with open(video2_path, "wb") as f:
                f.write(video2_file.read())

            # Load videos
            video1 = VideoFileClip(video1_path)
            video2 = VideoFileClip(video2_path)

            # Apply green→red filter to video2
            video2_red = video2.fl_image(green_to_red)

            # Overlay video2 on top of video1
            final = CompositeVideoClip([video1, video2_red.set_opacity(0.5)])

            # Export
            final.write_videofile(output_path, codec="libx264", audio_codec="aac")

            # Show result
            st.success("✅ Processing complete!")
            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button("Download Processed Video", f, file_name="output.mp4", mime="video/mp4")
