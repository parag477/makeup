import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
import av
import asyncio
from makeup_app import MakeupApplication  # Your MakeupApplication class

# Add all the provided STUN and TURN server configurations
rtc_configuration = RTCConfiguration({
    "iceServers": [
        {
            "urls": [
                "turn:numb.viagenie.ca",
                "turn:192.158.29.39:3478?transport=udp",
                "turn:192.158.29.39:3478?transport=tcp"
            ],
            "username": "webrtc@live.com", 
            "credential": "muazkh"
        },
        {
            "urls": [
                "turn:bn-turn2.xirsys.com:80?transport=udp",
                "turn:bn-turn2.xirsys.com:3478?transport=udp",
                "turn:bn-turn2.xirsys.com:80?transport=tcp",
                "turn:bn-turn2.xirsys.com:3478?transport=tcp",
                "turns:bn-turn2.xirsys.com:443?transport=tcp",
                "turns:bn-turn2.xirsys.com:5349?transport=tcp"
            ],
            "username": "41G6nRJn3PLi5np_1pjDKAtO9fygkHx94ENGd59gP28EvVonLQ10bXjIA5sxYcLIAAAAAGcINydwYXJhZzQ3Nw==",
            "credential": "275e088c-8745-11ef-9116-0242ac140004"
        }
    ]
})


# Processor class for applying virtual makeup
class VideoProcessor:
    def __init__(self):
        self.makeup_app = MakeupApplication()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")  # Convert frame to OpenCV format
        img = self.makeup_app.process_frame(img)  # Apply makeup filters
        return av.VideoFrame.from_ndarray(img, format="bgr24")  # Return processed frame

st.title("Virtual Makeup Applicatiosn xwith Webcam")

# Workaround for Streamlit's event loop issue
def create_event_loop():
    try:
        # Ensure an event loop is available in the current thread
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no loop is found, create a new one and set it
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

create_event_loop()


# Improved WebRTC streamer with TURN server and better error handling
webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,  # Enable both sending and receiving video
    video_processor_factory=VideoProcessor,  # Processor for applying makeup
    rtc_configuration=rtc_configuration,  # TURN server configuration to handle NAT/firewall issues
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},  # Ideal width
            "height": {"ideal": 720}   # Ideal height
        },
        "audio": False  # Disable audio
    },
    async_processing=False,  # Disable async processing for simplicity
)

# Provide a user-friendly message if connection fails
st.write("If you encounter issues, please check your network connectivity or TURN server.")
