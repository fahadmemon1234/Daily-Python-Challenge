import time
import streamlit as st
import threading
from playsound import playsound
from datetime import datetime, timedelta

# Apply CSS for Better UI
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            color: #ff5733;
            font-weight: bold;
        }
        .alarm-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            margin: 20px auto;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# UI Design
st.markdown('<p class="title">⏰ Advanced Alarm Clock</p>', unsafe_allow_html=True)

st.write("Set the alarm time (12-hour format)")

# Input Field
alarm_time = st.time_input("Select Alarm Time", value=None)
snooze_time = 5  # Default snooze time in minutes
alarm_active = False  # Check if alarm is active

online_custom_alarm_sound_input = st.text_input("Enter URL of Custom Alarm Sound", "https://www.soundjay.com/button/beep-07.wav") 

# Function to Play Alarm Sound
def play_alarm():
    try:
        playsound(online_custom_alarm_sound_input)  # Play the sound
    except Exception as e:
        st.error(f"Error playing alarm sound: {e}")


# Function to Beep Sound
def beep_alarm():
    try:
        for _ in range(3):  # Beep 3 times
            playsound("beep.mp3")
            time.sleep(1)
    except Exception as e:
        st.error(f"Error playing beep sound: {e}")


# Function to Check Alarm Time
def check_alarm():
    global alarm_active
    alarm_active = True  # Set alarm active
    while alarm_active:
        current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format
        if alarm_time and current_time == alarm_time.strftime("%I:%M %p"):
            st.markdown('<p class="success">⏰ Time\'s up! Wake up! 🔔</p>', unsafe_allow_html=True)
            threading.Thread(target=play_alarm).start()
            threading.Thread(target=beep_alarm).start()
            break
        time.sleep(1)


# Function to Snooze Alarm
def snooze_alarm():
    global alarm_time
    if alarm_time:
        new_alarm_time = (datetime.combine(datetime.today(), alarm_time) + timedelta(minutes=snooze_time)).time()
        st.success(f"🔄 Snoozed! New alarm set for {new_alarm_time.strftime('%I:%M %p')}")
        alarm_time = new_alarm_time
        threading.Thread(target=check_alarm).start()


# Button to Set Alarm
if st.button("Set Alarm", help="Click to activate alarm"):
    if alarm_time:
        st.success(f"✅ Alarm set for {alarm_time.strftime('%I:%M %p')}")
        threading.Thread(target=check_alarm).start()
    else:
        st.error("⚠️ Please select a valid time!")

# Button to Snooze Alarm
if st.button("Snooze", help="Click to snooze for 5 minutes"):
    snooze_alarm()

st.markdown('</div>', unsafe_allow_html=True)
