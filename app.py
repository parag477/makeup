import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import av
from makeup_app import MakeupApplication  # Your MakeupApplication class

from streamlit_webrtc import WebRtcMode, RTCConfiguration

rtc_configuration = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},  # Google's public STUN server
    ]
})

class VideoProcessor:
    def __init__(self):
        self.makeup_app = MakeupApplication()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = self.makeup_app.process_frame(img)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Virtual Makeup Application with Webcam")

# webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},
            "height": {"ideal": 720}
        },
        "audio": False
    }
)
