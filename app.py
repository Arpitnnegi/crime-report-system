import streamlit as st
from datetime import datetime
import pytz
import json
import pyperclip

# Set page config
st.set_page_config(
    page_title="UK Crime Reporting System",
    page_icon="🚔",
    layout="wide"
)

# Title
st.title("🚔 UK Crime Reporting System")
st.markdown("---")

# Initialize session state
if 'selected_crimes' not in st.session_state:
    st.session_state.selected_crimes = []
if 'report_type' not in st.session_state:
    st.session_state.report_type = "Gang"

# Crime lists
TOP_CHARGES = [
    "PC 3.1.6 Banditry",
    "PC 2.10.6 Robbery",
    "PC 2.8.3 Taking a hostage",
    "PC 2.5.6 Brandishing of a weapon",
    "PC 3.4.2 Trespassing in a State Facility",
    "PC 3.11 Murder or Attempted murder of a public servant"
]

ALL_CHARGES = [
    "PC 2.2.4 Cultivation of cannabis (small quantities)",
    "PC 2.2.5 Cultivation of cannabis (large quantities)",
    "PC 2.5.3 Open Carrying",
    "PC 2.5.8 Discharging a weapon in a public place",
    "PC 2.8.1 Abduction",
    "PC 2.8.2 Kidnapping",
    "PC 2.8.4 Human Trafficking",
    "PC 2.13.3 Vandalism",
    "PC 3.1.1 Participation in terrorism",
    "PC 3.1.4 Committing a terrorist act",
    "PC 3.1.5 Creation of a stable armed group",
    "PC 3.8.2 Impersonating a law enforcement officer",
    "PC 3.10 Battery of a public servant",
    "PC 3.20 Participation in a cyber attack of the state's resources"
]

# Layout
col1, col2 = st.columns(2)

with col1:
    # Report Type
    report_type = st.radio("**Select Report Type:**", ["Gang", "Family"])
    st.session_state.report_type = report_type
    
    # Basic Information
    st.subheader("Basic Information")
    name = st.text_input("**Name:**", key="name")
    crime_type = st.text_input("**Crime Type:**", key="crime_type")
    
    # Date and Time
    col1_date, col2_date = st.columns(2)
    with col1_date:
        date_input = st.date_input("**Date:**", value=datetime.now())
        date = date_input.strftime("%d.%m.%Y")
    with col2_date:
        time_input = st.time_input("**Time (24h):**", value=datetime.now().time())
        time = time_input.strftime("%H:%M")

with col2:
    # Crimes Selection
    st.subheader("Select Crimes")
    
    # Multi-select for crimes
    selected_top = st.multiselect("**Top Charges:**", TOP_CHARGES)
    selected_all = st.multiselect("**All Charges:**", ALL_CHARGES)
    
    # Combine selections
    all_selected = list(set(selected_top + selected_all))
    st.session_state.selected_crimes = all_selected
    
    # Display selected crimes
    if st.session_state.selected_crimes:
        st.write("**Selected Crimes:**")
        for crime in st.session_state.selected_crimes:
            st.write(f"• {crime}")
    else:
        st.write("No crimes selected")

# Evidence Links
st.markdown("---")
st.subheader("Evidence Links")

if report_type == "Gang":
    gang_proof = st.text_input("Proof of bodycam / refresh / upload:")
    gang_footage = st.text_input("Bodycam Footage:")
    gang_interrogation = st.text_input("Bodycam Footage of interrogation:")
    gang_id = st.text_input("Culprit Identification Proof:")
    gang_plates = st.text_input("License plates:")
    
    fields = {
        "Proof of bodycam / refresh / upload:": gang_proof,
        "Bodycam Footage:": gang_footage,
        "Bodycam Footage of interrogation:": gang_interrogation,
        "Culprit Identification Proof:": gang_id,
        "License plates:": gang_plates
    }
else:
    family_proof = st.text_input("Proof of bodycam / refresh / upload:")
    family_footage = st.text_input("Bodycam Footage:")
    family_id = st.text_input("Culprit Identification Proof:")
    family_interrogation = st.text_input("Bodycam Footage of interrogation:")
    family_plates = st.text_input("License plates:")
    family_pda = st.text_input("License plates searched in PDA:")
    family_owner = st.text_input("Owner of the car searched in PDA:")
    
    fields = {
        "Proof of bodycam / refresh / upload:": family_proof,
        "Bodycam Footage:": family_footage,
        "Culprit Identification Proof:": family_id,
        "Bodycam Footage of interrogation:": family_interrogation,
        "License plates:": family_plates,
        "License plates searched in PDA:": family_pda,
        "Owner of the car searched in PDA:": family_owner
    }

# Generate Report Button
st.markdown("---")
if st.button("📋 Generate Report", type="primary", use_container_width=True):
    if not name:
        st.error("Please enter a Name")
    else:
        # Part 1
        part1 = f"{name} | {crime_type} | {date} | {time}\n\n"
        
        # Part 2
        part2 = f"{report_type} Name: {name}\n\n"
        part2 += "=" * 50 + "\n"
        
        # Add fields
        for label, value in fields.items():
            value = value.strip()
            if value:
                part2 += f"{label}\n{value}\n"
            else:
                part2 += f"{label} N/A\n"
            part2 += "=" * 50 + "\n"
        
        # Add Crimes
        part2 += "Crimes Committed "
        part2 += "(Mandatory):\n" if report_type == "Gang" else ":\n"
        
        if st.session_state.selected_crimes:
            for crime in st.session_state.selected_crimes:
                part2 += f"- {crime}\n"
        else:
            part2 += "N/A\n"
        
        part2 += "=" * 50 + "\n"
        
        # Display output
        st.markdown("---")
        st.subheader("Generated Report")
        
        # Create tabs for different parts
        tab1, tab2, tab3 = st.tabs(["Full Report", "Part 1", "Part 2"])
        
        with tab1:
            full_report = part1 + part2
            st.code(full_report, language="text")
            
            # Download button
            st.download_button(
                label="💾 Download Report",
                data=full_report,
                file_name=f"{name}_{date.replace('.', '-')}.txt",
                mime="text/plain"
            )
        
        with tab2:
            st.code(part1.strip(), language="text")
            if st.button("📋 Copy Part 1", key="copy1"):
                st.write("Copied to clipboard!")
                # In Streamlit Cloud, use st.write for copy
                st.code(part1.strip())
        
        with tab3:
            st.code(part2.strip(), language="text")
            if st.button("📋 Copy Part 2", key="copy2"):
                st.write("Copied to clipboard!")
                st.code(part2.strip())

# Clear Button
if st.button("🔄 Clear All", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Requirements file
with open("requirements.txt", "w") as f:
    f.write("""streamlit==1.28.0
pytz==2023.3
pyperclip==1.8.2
""")