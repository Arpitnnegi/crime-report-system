import streamlit as st
from datetime import datetime
import pytz

# Set page config
st.set_page_config(
    page_title="UK Crime Reporting System",
    page_icon="🚔",
    layout="wide"
)

# Title
st.title("🚔 UK Crime Reporting System")
st.markdown("---")

# Initialize session state for persistence
if 'selected_crimes' not in st.session_state:
    st.session_state.selected_crimes = []
if 'report_type' not in st.session_state:
    st.session_state.report_type = "Gang"
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'crime_type' not in st.session_state:
    st.session_state.crime_type = ""
if 'date' not in st.session_state:
    uk_now = datetime.now(pytz.timezone('Europe/London'))
    st.session_state.date = uk_now.strftime("%d.%m.%Y")
if 'time' not in st.session_state:
    uk_now = datetime.now(pytz.timezone('Europe/London'))
    st.session_state.time = uk_now.strftime("%H:%M")
if 'nov_checked' not in st.session_state:
    st.session_state.nov_checked = False
if 'fields' not in st.session_state:
    st.session_state.fields = {}
if 'generated_report' not in st.session_state:
    st.session_state.generated_report = False
if 'part1' not in st.session_state:
    st.session_state.part1 = ""
if 'part2' not in st.session_state:
    st.session_state.part2 = ""

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
    # Report Type - updates session state
    st.subheader("Select Report Type:")
    report_type = st.radio(
        "", 
        ["Gang", "Family"],
        index=0 if st.session_state.report_type == "Gang" else 1,
        key="report_type_selector",
        label_visibility="collapsed",
        horizontal=True
    )
    
    # Update session state when changed
    if report_type != st.session_state.report_type:
        st.session_state.report_type = report_type
        # Reset fields when type changes
        st.session_state.fields = {}
    
    # Basic Information with session state
    st.subheader("Basic Information")
    
    name = st.text_input(
        "**Name:**", 
        value=st.session_state.name,
        key="name_input"
    )
    st.session_state.name = name
    
    st.subheader("Crime Type:")
    
    crime_type = st.text_input(
        "", 
        value=st.session_state.crime_type,
        key="crime_type_input",
        label_visibility="collapsed"
    )
    st.session_state.crime_type = crime_type
    
    # Date and Time - FIXED: Now editable and persistent
    col_date, col_time = st.columns(2)
    
    with col_date:
        # Date input - editable and persistent
        date_input = st.text_input(
            "**Date (DD.MM.YYYY):**",
            value=st.session_state.date,
            key="date_input"
        )
        st.session_state.date = date_input
        
        if st.button("📅 Set to Now", key="date_now", use_container_width=True):
            uk_now = datetime.now(pytz.timezone('Europe/London'))
            st.session_state.date = uk_now.strftime("%d.%m.%Y")
            st.rerun()
    
    with col_time:
        # Time input - FIXED: Changed label and made persistent
        time_input = st.text_input(
            "**Time (24h HH:MM):**",  # FIXED LABEL
            value=st.session_state.time,
            key="time_input"
        )
        st.session_state.time = time_input
        
        if st.button("⏰ Set to Now", key="time_now", use_container_width=True):
            uk_now = datetime.now(pytz.timezone('Europe/London'))
            st.session_state.time = uk_now.strftime("%H:%M")
            st.rerun()
    
    # NOV Checkbox - FIXED: Added to session state
    st.subheader("NOV:")
    nov_checked = st.checkbox(
        "",
        value=st.session_state.nov_checked,
        key="nov_checkbox"
    )
    st.session_state.nov_checked = nov_checked

with col2:
    # Crimes Selection - FIXED: Using multiselect which stays open
    st.subheader("Select Crimes")
    
    st.markdown("**Top Charges:**")
    # FIXED: Using multiselect with key to prevent closing
    selected_top = st.multiselect(
        "", 
        TOP_CHARGES,
        default=[c for c in TOP_CHARGES if c in st.session_state.selected_crimes],
        key="top_charges",
        label_visibility="collapsed"
    )
    
    st.markdown("**All Charges:**")
    selected_all = st.multiselect(
        "", 
        ALL_CHARGES,
        default=[c for c in ALL_CHARGES if c in st.session_state.selected_crimes],
        key="all_charges",
        label_visibility="collapsed"
    )
    
    # Combine selections and update session state
    all_selected = list(set(selected_top + selected_all))
    st.session_state.selected_crimes = all_selected
    
    # Display selected crimes
    if st.session_state.selected_crimes:
        st.markdown("**Selected Crimes:**")
        for crime in st.session_state.selected_crimes:
            st.markdown(f"• {crime}")
    else:
        st.markdown("*No crimes selected*")

# Evidence Links - Dynamic fields based on report type
st.markdown("---")
st.subheader("Evidence Links")

# Initialize field keys if not exists
field_keys_gang = ["gang_proof", "gang_footage", "gang_interrogation", "gang_id", "gang_plates"]
field_keys_family = ["family_proof", "family_footage", "family_id", "family_interrogation", "family_plates", "family_pda", "family_owner"]

# Initialize all field values in session state
for key in field_keys_gang + field_keys_family:
    if key not in st.session_state.fields:
        st.session_state.fields[key] = ""

if report_type == "Gang":
    # Gang fields with proper label
    col1_fields, col2_fields = st.columns(2)
    
    with col1_fields:
        gang_proof = st.text_area(
            "**Proof of bodycam / refresh / upload:**", 
            value=st.session_state.fields.get("gang_proof", ""),
            key="gang_proof_input",
            height=100
        )
        st.session_state.fields["gang_proof"] = gang_proof
        
        gang_footage = st.text_area(
            "**Bodycam Footage:**", 
            value=st.session_state.fields.get("gang_footage", ""),
            key="gang_footage_input",
            height=100
        )
        st.session_state.fields["gang_footage"] = gang_footage
        
        gang_interrogation = st.text_area(
            "**Bodycam Footage of interrogation:**", 
            value=st.session_state.fields.get("gang_interrogation", ""),
            key="gang_interrogation_input",
            height=100
        )
        st.session_state.fields["gang_interrogation"] = gang_interrogation
    
    with col2_fields:
        gang_id = st.text_area(
            "**Culprit Identification Proof:**", 
            value=st.session_state.fields.get("gang_id", ""),
            key="gang_id_input",
            height=100
        )
        st.session_state.fields["gang_id"] = gang_id
        
        gang_plates = st.text_area(
            "**License plates:**", 
            value=st.session_state.fields.get("gang_plates", ""),
            key="gang_plates_input",
            height=100
        )
        st.session_state.fields["gang_plates"] = gang_plates
    
    fields_display = {
        "Proof of bodycam / refresh / upload:": gang_proof,
        "Bodycam Footage:": gang_footage,
        "Bodycam Footage of interrogation:": gang_interrogation,
        "Culprit Identification Proof:": gang_id,
        "License plates:": gang_plates
    }
else:
    # Family fields
    col1_fields, col2_fields = st.columns(2)
    
    with col1_fields:
        family_proof = st.text_area(
            "**Proof of bodycam / refresh / upload:**", 
            value=st.session_state.fields.get("family_proof", ""),
            key="family_proof_input",
            height=80
        )
        st.session_state.fields["family_proof"] = family_proof
        
        family_footage = st.text_area(
            "**Bodycam Footage:**", 
            value=st.session_state.fields.get("family_footage", ""),
            key="family_footage_input",
            height=80
        )
        st.session_state.fields["family_footage"] = family_footage
        
        family_id = st.text_area(
            "**Culprit Identification Proof:**", 
            value=st.session_state.fields.get("family_id", ""),
            key="family_id_input",
            height=80
        )
        st.session_state.fields["family_id"] = family_id
        
        family_interrogation = st.text_area(
            "**Bodycam Footage of interrogation:**", 
            value=st.session_state.fields.get("family_interrogation", ""),
            key="family_interrogation_input",
            height=80
        )
        st.session_state.fields["family_interrogation"] = family_interrogation
    
    with col2_fields:
        family_plates = st.text_area(
            "**License plates:**", 
            value=st.session_state.fields.get("family_plates", ""),
            key="family_plates_input",
            height=80
        )
        st.session_state.fields["family_plates"] = family_plates
        
        family_pda = st.text_area(
            "**License plates searched in PDA:**", 
            value=st.session_state.fields.get("family_pda", ""),
            key="family_pda_input",
            height=80
        )
        st.session_state.fields["family_pda"] = family_pda
        
        family_owner = st.text_area(
            "**Owner of the car searched in PDA:**", 
            value=st.session_state.fields.get("family_owner", ""),
            key="family_owner_input",
            height=80
        )
        st.session_state.fields["family_owner"] = family_owner
    
    fields_display = {
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
generate_col1, generate_col2 = st.columns([3, 1])

with generate_col1:
    if st.button("📋 Generate Report", type="primary", use_container_width=True):
        if not st.session_state.name:
            st.error("Please enter a Name")
        else:
            # Part 1
            nov_text = "Nov" if st.session_state.nov_checked else ""
            part1 = f"{st.session_state.name} | {st.session_state.crime_type} | {st.session_state.date} {st.session_state.time} {nov_text}\n\n"
            
            # Part 2
            part2 = f"{report_type} Name: {st.session_state.name}\n\n"
            part2 += "=" * 50 + "\n"
            
            # Add fields
            for label, value in fields_display.items():
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
            st.session_state.generated_report = True
            
            st.success("✅ Report generated successfully!")

with generate_col2:
    if st.button("🔄 Clear All", use_container_width=True):
        # FIXED: Clear everything properly
        st.session_state.selected_crimes = []
        st.session_state.name = ""
        st.session_state.crime_type = ""
        
        # Reset date and time to now
        uk_now = datetime.now(pytz.timezone('Europe/London'))
        st.session_state.date = uk_now.strftime("%d.%m.%Y")
        st.session_state.time = uk_now.strftime("%H:%M")
        
        st.session_state.nov_checked = False
        st.session_state.fields = {}
        st.session_state.generated_report = False
        st.session_state.part1 = ""
        st.session_state.part2 = ""
        st.session_state.full_report = ""
        
        st.rerun()

# Display generated report (if exists) - PERSISTENT
if st.session_state.generated_report:
    st.markdown("---")
    st.subheader("📄 Generated Report")
    
    # Create tabs for different parts
    tab1, tab2, tab3 = st.tabs(["📋 Full Report", "1️⃣ Part 1", "2️⃣ Part 2"])
    
    with tab1:
        st.code(st.session_state.full_report, language="text")
        
        # Download button
        st.download_button(
            label="💾 Download Full Report",
            data=st.session_state.full_report,
            file_name=f"{st.session_state.name}_{st.session_state.date.replace('.', '-')}_report.txt",
            mime="text/plain",
            key="download_full"
        )
    
    with tab2:
        st.code(st.session_state.part1.strip(), language="text")
        
        # Copy feedback without clearing form
        if st.button("📋 Copy Part 1", key="copy_part1", use_container_width=True):
            st.code(st.session_state.part1.strip())
            st.success("✅ Part 1 ready to copy! Select and copy the text above.")
    
    with tab3:
        st.code(st.session_state.part2.strip(), language="text")
        
        if st.button("📋 Copy Part 2", key="copy_part2", use_container_width=True):
            st.code(st.session_state.part2.strip())
            st.success("✅ Part 2 ready to copy! Select and copy the text above.")

# Instructions
with st.expander("📖 How to use this app"):
    st.markdown("""
    ### **Steps to use:**
    1. **Select** Gang or Family report type
    2. **Enter** Name and Crime Type
    3. **Enter/Edit** Date and Time (use Now buttons or type manually)
    4. **Select** crimes from the lists (select multiple without closing)
    5. **Check** NOV if needed
    6. **Paste** ImgBB links in evidence fields
    7. **Click** "Generate Report"
    8. **Use tabs** to view/copy different parts
    9. **Download** the full report
    
    ### **Fixed Issues:**
    - ✅ **Time label corrected** from "Job hit" to "24h HH:MM"
    - ✅ **Multiselect stays open** when adding charges
    - ✅ **Date and time work** and are editable
    - ✅ **Clear button clears** everything including NOV checkbox
    - ✅ **NOV checkbox added** and works correctly
    
    ### **Note about copying:**
    - Select the text and **Ctrl+C** to copy
    - Or use **Download button** to save as file
    - Form stays filled after copying
    """)

# Footer
st.markdown("---")
st.caption("UK Crime Reporting System v3.0 | All issues fixed | Data persists in this session")