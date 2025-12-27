import streamlit as st

# ---------------- Patient Class ----------------
class Patient:
    def __init__(self, name, age, disease, patient_id):
        self.name = name
        self.age = age
        self.disease = disease
        self.patient_id = patient_id


# ---------------- Session Storage ----------------
if "patients" not in st.session_state:
    st.session_state.patients = {}


# ---------------- Dashboard UI ----------------
st.set_page_config(page_title="Hospital Dashboard", layout="centered")
st.title("🏥 Hospital Patient Management System")

menu = st.sidebar.selectbox(
    "Dashboard Menu",
    ["Add Patient", "Search Patient", "Show All Patients"]
)

# ---------------- Add Patient ----------------
if menu == "Add Patient":
    st.subheader("➕ Add New Patient")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    disease = st.text_input("Disease")
    patient_id = st.text_input("Patient ID")

    if st.button("Add Patient"):
        if patient_id in st.session_state.patients:
            st.error("❌ Patient ID already exists!")
        elif name == "" or disease == "" or patient_id == "":
            st.warning("⚠️ Please fill all fields")
        else:
            st.session_state.patients[patient_id] = Patient(
                name, age, disease, patient_id
            )
            st.success("✅ Patient Added Successfully!")

# ---------------- Search Patient ----------------
elif menu == "Search Patient":
    st.subheader("🔍 Search Patient")

    search_id = st.text_input("Enter Patient ID")

    if st.button("Search"):
        patient = st.session_state.patients.get(search_id)

        if patient:
            st.info("Patient Found")
            st.write(f"**ID:** {patient.patient_id}")
            st.write(f"**Name:** {patient.name}")
            st.write(f"**Age:** {patient.age}")
            st.write(f"**Disease:** {patient.disease}")
        else:
            st.error("❌ Patient Not Found")

# ---------------- Show All Patients ----------------
elif menu == "Show All Patients":
    st.subheader("📋 All Patients")

    if not st.session_state.patients:
        st.warning("⚠️ No patients available")
    else:
        for patient in st.session_state.patients.values():
            st.markdown("---")
            st.write(f"**ID:** {patient.patient_id}")
            st.write(f"**Name:** {patient.name}")
            st.write(f"**Age:** {patient.age}")
            st.write(f"**Disease:** {patient.disease}")
