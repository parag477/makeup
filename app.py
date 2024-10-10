import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
import av
import logging
from makeup_app import MakeupApplication  # Your MakeupApplication class

# Set up logging to troubleshoot issues
logging.basicConfig(level=logging.DEBUG)

# RTC configuration (STUN server for now, you can add TURN if needed)
rtc_configuration = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun1.l.google.com:19302"]},  # Google's public STUN server
    ]
})

class VideoProcessor:
    def __init__(self):
        try:
            self.makeup_app = MakeupApplication()  # Initialize the makeup application
        except Exception as e:
            logging.error(f"Error initializing MakeupApplication: {str(e)}")
            self.makeup_app = None

    def recv(self, frame):
        try:
            # Convert the received frame to a numpy array
            img = frame.to_ndarray(format="bgr24")
            
            # Check if the makeup application initialized successfully
            if self.makeup_app:
                img = self.makeup_app.process_frame(img)
            else:
                logging.error("MakeupApplication is not initialized properly")
            
            # Return the processed frame
            return av.VideoFrame.from_ndarray(img, format="bgr24")
        except Exception as e:
            logging.error(f"Error processing video frame: {str(e)}")
            return frame  # Return the original frame in case of error

st.title("Virtual Makeup Application with Webcam tst")

# WebRTC video streamer
webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,  # Ensure it both sends and receives video streams
    rtc_configuration=rtc_configuration,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},
            "height": {"ideal": 720}
        },
        "audio": False
    },
    async_processing=True  # Use async processing for better performance
)
