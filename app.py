import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import av
from makeup_app import MakeupApplication  # Your MakeupApplication class

class VideoProcessor:
    def __init__(self):
        self.makeup_app = MakeupApplication()

    def recv(self, frame):
        # Convert frame to ndarray (image) and process it using MakeupApplication
        img = frame.to_ndarray(format="bgr24")
        img = self.makeup_app.process_frame(img)  # Apply makeup filter
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Virtual Makeup Application with Webcam")

# Basic WebRTC streamer with default settings
webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,  # Enable video sending and receiving
    video_processor_factory=VideoProcessor,  # Use the VideoProcessor for applying makeup
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},  # Ideal video width
            "height": {"ideal": 720}   # Ideal video height
        },
        "audio": False  # Disable audio for simplicity
    },
    async_processing=False  # Disable asynchronous processing for now
)
