import streamlit as st
from datetime import datetime
import pytz
import json

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
    col1_fields, col2_fields = st.columns(2)
    
    with col1_fields:
        gang_proof = st.text_input("Proof of bodycam / refresh / upload:", key="gang_proof")
        gang_footage = st.text_input("Bodycam Footage:", key="gang_footage")
        gang_interrogation = st.text_input("Bodycam Footage of interrogation:", key="gang_interrogation")
    
    with col2_fields:
        gang_id = st.text_input("Culprit Identification Proof:", key="gang_id")
        gang_plates = st.text_input("License plates:", key="gang_plates")
    
    fields = {
        "Proof of bodycam / refresh / upload:": gang_proof,
        "Bodycam Footage:": gang_footage,
        "Bodycam Footage of interrogation:": gang_interrogation,
        "Culprit Identification Proof:": gang_id,
        "License plates:": gang_plates
    }
else:
    col1_fields, col2_fields = st.columns(2)
    
    with col1_fields:
        family_proof = st.text_input("Proof of bodycam / refresh / upload:", key="family_proof")
        family_footage = st.text_input("Bodycam Footage:", key="family_footage")
        family_id = st.text_input("Culprit Identification Proof:", key="family_id")
        family_interrogation = st.text_input("Bodycam Footage of interrogation:", key="family_interrogation")
    
    with col2_fields:
        family_plates = st.text_input("License plates:", key="family_plates")
        family_pda = st.text_input("License plates searched in PDA:", key="family_pda")
        family_owner = st.text_input("Owner of the car searched in PDA:", key="family_owner")
    
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
        
        # Store in session state
        st.session_state.part1 = part1
        st.session_state.part2 = part2
        st.session_state.full_report = part1 + part2
        
        # Display output
        st.markdown("---")
        st.subheader("✅ Report Generated Successfully!")
        
        # Create tabs for different parts
        tab1, tab2, tab3 = st.tabs(["📄 Full Report", "1️⃣ Part 1", "2️⃣ Part 2"])
        
        with tab1:
            st.code(st.session_state.full_report, language="text")
            
            # Download button
            st.download_button(
                label="💾 Download Full Report",
                data=st.session_state.full_report,
                file_name=f"{name}_{date.replace('.', '-')}.txt",
                mime="text/plain"
            )
        
        with tab2:
            st.code(st.session_state.part1.strip(), language="text")
            
            # Copy button using Streamlit's copy function
            if st.button("📋 Copy Part 1", key="copy1", use_container_width=True):
                st.code(st.session_state.part1.strip())
                st.success("✅ Part 1 ready to copy! Select and copy the text above.")
        
        with tab3:
            st.code(st.session_state.part2.strip(), language="text")
            
            if st.button("📋 Copy Part 2", key="copy2", use_container_width=True):
                st.code(st.session_state.part2.strip())
                st.success("✅ Part 2 ready to copy! Select and copy the text above.")

# Clear Button
if st.button("🔄 Clear All", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Instructions
with st.expander("📖 How to use this app"):
    st.markdown("""
    ### **Steps to use:**
    1. **Select** Gang or Family report type
    2. **Enter** Name and Crime Type
    3. **Select** crimes from the lists
    4. **Paste** ImgBB links in evidence fields
    5. **Click** "Generate Report"
    6. **Use tabs** to view/copy different parts
    7. **Download** the full report
    
    ### **Note about copying:**
    - In web browsers, you need to **select the text** and **Ctrl+C**
    - Or use the **Download button** to save as file
    - Part 1: `Name | Crime | Date | Time`
    - Part 2: Evidence links and crimes list
    """)