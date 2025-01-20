import streamlit as st
import pandas as pd
import random
import time

# Set up the page configuration
st.set_page_config(page_title="Random Winner Picker", page_icon="🎉", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
        font-family: "Arial", sans-serif;
        color: #333;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title("🎉 Winner Picker App 🎉")
st.markdown("Upload a CSV or Excel file to select a winner!")

# File Upload
uploaded_file = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        st.write("Uploaded data preview:")
        st.write(data.head())  # Display the first few rows of the uploaded data
        st.write("Column names detected:", data.columns.tolist())  # Display detected column names
        st.write("Rows where Attendance is TRUE:")
        st.write(data[data['Attendance'] == 1])  # Adjust based on your case sensitivity

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
                st.write("🎉 Picking a winner... 🎉")
                placeholder = st.empty()

                # Flash through names
                for _ in range(30):  # Adjust the range for longer animations
                    random_name = random.choice(names)
                    placeholder.markdown(f"<h1 style='text-align: center; color: #FF5733;'>{random_name}</h1>", unsafe_allow_html=True)
                    time.sleep(0.1)  # Adjust speed for animation

            # Final winner
                winner = random.choice(names)
                placeholder.markdown(f"<h1 style='text-align: center; color: #28A745;'>🎉 {winner} 🎉</h1>", unsafe_allow_html=True)
                st.balloons()

            # if st.button("🎲 Pick a Winner!"):
            #     if not valid_data.empty:
            #         with st.spinner("Spinning..."):
            #             time.sleep(random.uniform(3, 8))
            #             selected_row = valid_data.sample(n=1).iloc[0]
            #             selected_name = f"{selected_row[first_name_col]} {selected_row[last_name_col]}"
            #             st.balloons()
            #             st.success(f"🎉 And the winner is...: {selected_name}")
            else:
                st.error("No valid names to choose from. Make sure the attendance column has TRUE values.")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
