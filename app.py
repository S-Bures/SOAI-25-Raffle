import streamlit as st
import pandas as pd
import random
import time
import base64

# Set up the page configuration
st.set_page_config(page_title="RAFI (Randomised Automated Fariness Initiative)", page_icon= "static/Nexus_IRIS.png", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #523b88;
        font-family: "Arial", sans-serif;
        color: #333;
    }
    .stButton button {
        background-color: #523b88;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("static/logo_full.png", use_container_width=True)


# Add your image to the top left corner
# st.markdown("""
#     <style>
#     [data-testid="stAppViewContainer"] {
#         position: relative;
#     }
#     .logo-container {
#         position: absolute;
#         top: 10px;
#         left: 10px;
#         z-index: 1000;
#     }
#     .logo-container img {
#         width: 80px; /* Adjust the size as needed */
#     }
#     </style>
#     <div class="logo-container">
#         <img src="static/logo_full.png" alt=" ">
#     </div>
# """, unsafe_allow_html=True)



def play_audio():    
    # Streamlit's st.markdown to inject custom HTML for autoplay without controls
    audio_html = f"""
    <audio autoplay>
      <source src="data:audio/wav;base64,{get_audio_base64("static/tadaa.wav")}" type="audio/wav">
      Your browser does not support the audio element.
    </audio>
    """
    return audio_html


def get_audio_base64(file_path):
    """Convert the audio file to base64 to embed it in the app."""
    with open(file_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
    return audio_base64



# Title and Description
st.title("🎉 RAFI (Randomised Automated Fariness Initiative) 🎉")
st.markdown("Upload a CSV or Excel file to select a winner!")

# File Upload
uploaded_file = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"])

# Store whether the button was clicked
# if "button_clicked" not in st.session_state:
#     st.session_state.button_clicked = False



if uploaded_file:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        # st.write("Uploaded data preview:")
        # st.write(data.head())  # Display the first few rows of the uploaded data
        # st.write("Column names detected:", data.columns.tolist())  # Display detected column names
        # st.write("Rows where Attendance is TRUE:")
        # st.write(data[data['Attendance'] == 1])  

        # Normalize column names (case-insensitive)
        data.columns = [col.strip().lower() for col in data.columns]

        # Identify necessary columns
        first_name_col = next((col for col in data.columns if "first" in col), None)
        last_name_col = next((col for col in data.columns if "last" in col), None)
        attendance_col = next((col for col in data.columns if "attendance" in col), None)


        # Check if all required columns are present
        if not first_name_col or not last_name_col or not attendance_col:
            st.error("Missing required columns: first name, last name, or attendance.")
        else:
            # Filter data where attendance is TRUE
            valid_data = data[data[attendance_col] == 1]

            # Display the filtered data
            st.dataframe(valid_data[[first_name_col, last_name_col]])

            names = list(valid_data[first_name_col] + " " + valid_data[last_name_col])
            # Random Name Picker
            

            if st.button("Pick a Winner!"):
                # Set session state to indicate button was clicked
                # st.session_state.button_clicked = True

                audio_html = play_audio()
                st.markdown(audio_html, unsafe_allow_html=True)
                st.write("🎉 Picking a winner... 🎉")
                placeholder = st.empty()

                # Flash through names
                for _ in range(37):  # Adjust the range for longer animations
                    random_name = random.choice(names)
                    placeholder.markdown(f"<h1 style='text-align: center; color: #FF5733;'>{random_name}</h1>", unsafe_allow_html=True)
                    time.sleep(0.1)  # Adjust speed for animation

            # Final winner
                winner = random.choice(names)
                placeholder.markdown(f"<h1 style='text-align: center; color: #28A745;'>🎉 {winner} 🎉</h1>", unsafe_allow_html=True)
                st.balloons()

            
            else:
                st.error("")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
