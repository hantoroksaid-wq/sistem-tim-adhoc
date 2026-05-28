import streamlit as st
import pandas as pd
from datetime import date

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Informasi Kerja Tim Adhoc",
    page_icon="📊",
    layout="wide"
)

# --- SIMULASI DATABASE USER (LOGIN GOOGLE) ---
# Mengakomodasi instruksi login menggunakan username/password (simulasi akun Google)
USER_CREDENTIALS = {
    "ferdy@alumni.ac.id": {"nama": "Dosen Ferdy", "role": "PIC PDBA"},
    "han@alumni.ac.id": {"nama": "Han", "role": "PIC Tracer Study"},
    "senior@alumni.ac.id": {"nama": "Dosen Senior", "role": "Admin/Supervising"}
}

# --- INITIAL STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'tasks' not in st.session_state:
    # Data Berdasarkan Kerangka Kerja Dosen Senior
    st.session_state.tasks = [
        {"Tahapan": "Kick Off: Prototype PDBA", "PIC": "Dosen Ferdy", "Status": "Selesai", "Target": "2026-05-25"},
        {"Tahapan": "Kick Off: Prototype Tracer Study", "PIC": "Han", "Status": "Selesai", "Target": "2026-05-25"},
        {"Tahapan": "Rencana Implementasi: Integrasi Domain", "PIC": "Han", "Status": "Proses", "Target": "2026-06-01"},
        {"Tahapan": "Rencana Implementasi: Akun Dashboard Tracer", "PIC": "Han", "Status": "Belum Mulai", "Target": "2026-06-03"},
        {"Tahapan": "Rencana Implementasi: Koordinasi Rekening PDBA (Muamalat/BMU)", "PIC": "Dosen Ferdy", "Status": "Proses", "Target": "2026-05-30"},
        {"Tahapan": "Rencana Implementasi: Database Donatur", "PIC": "Dosen Ferdy", "Status": "Belum Mulai", "Target": "2026-06-05"},
        {"Tahapan": "Uji Coba Sistem: Website PDBA", "PIC": "Dosen Ferdy", "Status": "Belum Mulai", "Target": "2026-06-08"},
        {"Tahapan": "Uji Coba Sistem: Dashboard Tracer Study", "PIC": "Han", "Status": "Belum Mulai", "Target": "2026-06-08"},
        {"Tahapan": "Perbaikan Sistem", "PIC": "Tim Adhoc", "Status": "Belum Mulai", "Target": "2026-06-12"},
        {"Tahapan": "Launching Sistem", "PIC": "Dosen Senior", "Status": "Belum Mulai", "Target": "2026-06-15"},
        {"Tahapan": "Pelaksanaan & Monitoring", "PIC": "Tim Adhoc", "Status": "Belum Mulai", "Target": "2026-06-20"},
        {"Tahapan": "Evaluasi Berkala: Partisipasi Donatur & Tracer", "PIC": "Dosen Senior", "Status": "Belum Mulai", "Target": "2026-07-01"},
    ]

# --- HALAMAN LOGIN ---
def login_page():
    st.title("🔒 Login Sistem Informasi Kerja")
    st.subheader("Tim Adhoc Alumni & Tracer Study")
    st.write("Silakan login menggunakan akun Google/Email tim Anda.")
    
    email = st.text_input("Username / Email Google", placeholder="contoh: ferdy@alumni.ac.id")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    if st.button("Log In via Google Account", type="primary"):
        if email in USER_CREDENTIALS:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Akun tidak terdaftar dalam Tim Adhoc. Periksa kembali email Anda.")

# --- HALAMAN UTAMA (DASHBOARD) ---
def main_page():
    user_info = USER_CREDENTIALS[st.session_state.user_email]
    
    # Sidebar Info Pengguna
    st.sidebar.title("📌 SIK Tim Adhoc")
    st.sidebar.write(f"**Pengguna:** {user_info['nama']}")
    st.sidebar.write(f"**Role:** {user_info['role']}")
    if st.sidebar.button("Log Out", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()
        
    st.title("📊 Dashboard Kerja Tim Adhoc")
    st.info("🗓️ **Target Launching Sistem: 15 Juni 2026**")
    
    # Ringkasan Statis (Metrics)
    df = pd.DataFrame(st.session_state.tasks)
    total_tugas = len(df)
    selesai = len(df[df["Status"] == "Selesai"])
    proses = len(df[df["Status"] == "Proses"])
    belum = len(df[df["Status"] == "Belum Mulai"])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Tahapan", total_tugas)
    m2.metric("Selesai ✅", selesai)
    m3.metric("Dalam Proses ⏳", proses)
    m4.metric("Belum Mulai 🛑", belum)
    
    st.write("---")
    
    # Navigasi Menu Dalam Aplikasi
    menu = st.tabs(["📋 Alur Kerja & PIC", "✏️ Update Progress Task", "💾 Database Donatur & Tracer"])
    
    # TAB 1: Tabel Alur Kerja
    with st.sidebar:
        st.subheader("Kerangka Kerja & Penanggung Jawab (PIC)")
        st.dataframe(df, use_container_width=True)
        
    # TAB 2: Update Progress (Hanya PIC bersangkutan atau Admin yang bisa ubah)
    with menu:
        st.subheader("Update Status Pelaksanaan Komponen")
        task_names = [t["Tahapan"] for t in st.session_state.tasks]
        selected_task = st.selectbox("Pilih Tahapan Kerja:", task_names)
        
        # Ambil data index task yang dipilih
        idx = task_names.index(selected_task)
        current_task = st.session_state.tasks[idx]
        
        st.write(f"**PIC Saat Ini:** {current_task['PIC']}")
        
        # Validasi Akses Edit (Kritik Keamanan)
        if user_info['role'] == "Admin/Supervising" or user_info['nama'] == current_task['PIC'] or current_task['PIC'] == "Tim Adhoc":
            new_status = st.selectbox("Ubah Status:", ["Belum Mulai", "Proses", "Selesai"], index=["Belum Mulai", "Proses", "Selesai"].index(current_task['Status']))
            new_pic = st.text_input("Sesuaikan PIC jika diperlukan:", value=current_task['PIC'])
            
            if st.button("Simpan Perubahan"):
                st.session_state.tasks[idx]["Status"] = new_status
                st.session_state.tasks[idx]["PIC"] = new_pic
                st.success(f"Berhasil memperbarui tahapan: {selected_task}")
                st.rerun()
        else:
            st.warning("Anda tidak memiliki akses untuk mengubah tahapan ini karena Anda bukan PIC yang ditunjuk.")

    # TAB 3: Rencana Fitur Database & Akun (Rencana Implementasi)
    with menu:
        st.subheader("Status Koordinasi & Akun Sistem")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🏦 Status Rekening PDBA
            * **Opsi Saat Ini:** Bank Muamalat vs Bank Syariah Indonesia (BMU).
            * **Status Kordinasi:** Menunggu keputusan rapat dosen senior.
            """)
            st.radio("Rekomendasi Tim Kerja:", ["Tetap di Bank Muamalat (Akun Lama)", "Migrasi ke BMU"], index=0)
            
        with col2:
            st.markdown("""
            ### 👥 Integrasi Database Donatur
            * *Skema enkripsi password akun pelacak telah disiapkan.*
            * *Target penarikan data alumni aktif:* Selesai sebelum uji coba website 8 Juni 2026.
            """)
            st.text_input("Link Spreadsheet/Database Dummy (jika ada):", placeholder="https://docs.google.com/spreadsheets/...")

# --- ROUTING HALAMAN ---
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        main_page()
