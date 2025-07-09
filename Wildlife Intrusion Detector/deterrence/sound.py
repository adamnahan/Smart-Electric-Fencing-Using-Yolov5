import os
import playsound

def play_sound():  # Changed from play_deterrent_sound to play_sound
    try:
        # Get the absolute path to the alarm.mp3 file
        # Looking for alarm.mp3 in the parent directory (same level as main.py)
        alarm_path = os.path.join(os.path.dirname(__file__), '..', 'alarm.mp3')
        alarm_path = os.path.abspath(alarm_path)
        
        # Check if file exists
        if os.path.exists(alarm_path):
            print(f"Playing sound from: {alarm_path}")
            playsound.playsound(alarm_path)
        else:
            print(f"Sound file not found at: {alarm_path}")
            # Fallback: try in the deterrence directory
            local_alarm = os.path.join(os.path.dirname(__file__), 'alarm.mp3')
            if os.path.exists(local_alarm):
                print(f"Playing sound from: {local_alarm}")
                playsound.playsound(local_alarm)
            else:
                print("ERROR: alarm.mp3 not found!")
                print(f"Looked in: {alarm_path}")
                print(f"Also looked in: {local_alarm}")
                
    except Exception as e:
        print(f"Error playing sound: {e}")

# Keep the old function name for compatibility
def play_deterrent_sound():
    play_sound()