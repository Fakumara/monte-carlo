import streamlit as st
import pandas as pd
import mysql.connector
import numpy as np
import math
import scipy.stats as stats
import datetime
import locale
from calendar import monthrange
from datetime import timedelta, datetime
# def get_supplier_info(selected_material, connection):
#     query = f"SELECT * FROM supplier WHERE Nama_Material = '{selected_material}'"
#     df_sup = pd.read_sql(query, connection)
#     return df_sup

st.set_page_config(page_title="Dashboard App", page_icon="📊" , layout="wide")
# Koneksi ke database MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan username MySQL Anda
            password="",  # Ganti dengan password MySQL Anda
            database="db_simulasi"
        )
        return connection
    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
    return connection

# Fungsi untuk melakukan autentikasi OAuth
def authenticate(username, password):
    # Gantilah dengan logika autentikasi OAuth sesuai kebutuhan Anda
    # Di sini, kita hanya memeriksa apakah username dan password sesuai dengan yang diharapkan
    return username == "admin" and password == "admin_password"

# Halaman login
def login():
    st.sidebar.title("Login Dashboard 🔒")
    st.markdown("<h1 style='color: #1F2855;'>Dashboard Admin</h1>", unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.sidebar.success("Login berhasil!")
            else:
                st.sidebar.error("Login gagal. Coba lagi.")
    else:
        st.sidebar.info("Anda sudah login.  🔓")

    return st.session_state.logged_in

# Halaman admin setelah login
def admin_page():
    st.markdown("<h1 style='color: #0093AD;'>Database Page</h1>", unsafe_allow_html=True)

    # Buat koneksi ke database
    connection = create_connection()
    if connection:
        tab_database, tab_addform, tab_editform, tab_deleteform= st.tabs(["Database 📊", "Form Add Data 🆕", "Form Edit Data 📝", "Delete Data ❌"])
        with tab_database:
            # Ambil data Supplier dari database
            query_supplier = "SELECT * FROM supplier"
            df_supplier = pd.read_sql(query_supplier, connection)
            
            # Ambil data Suku Cadang dari database
            query_suku_cadang = "SELECT * FROM suku_cadang"
            df_suku_cadang = pd.read_sql(query_suku_cadang, connection)
            
            # Ambil data Permintaan dari database
            query_permintaan = "SELECT * FROM data_permintaan"
            df_permintaan = pd.read_sql(query_permintaan, connection)
            
            # Ambil data Pemesanan dari database
            query_pemesanan = "SELECT * FROM data_pemesanan"
            df_pemesanan = pd.read_sql(query_pemesanan, connection)
            
            # Ambil data Pemesanan dari database
            query_hasil = "SELECT * FROM hasil_simulasi"
            df_hasil = pd.read_sql(query_hasil, connection)

            # Tampilkan data menggunakan Streamlit
            st.markdown("<h3 style='color: #1F2855;'>Tabel Supplier 🏢</h3>", unsafe_allow_html=True)
            st.dataframe(df_supplier)
            st.markdown("<h3 style='color: #1F2855;'>Tabel Suku Cadang 🔩</h3>", unsafe_allow_html=True)
            st.dataframe(df_suku_cadang)
            st.markdown("<h3 style='color: #1F2855;'>Tabel Permintaan 📦</h3>", unsafe_allow_html=True)
            st.dataframe(df_permintaan)
            st.markdown("<h3 style='color: #1F2855;'>Tabel Pemesanan 📋</h3>", unsafe_allow_html=True)
            st.dataframe(df_pemesanan)
            st.markdown("<h3 style='color: #1F2855;'>Tabel Hasil Simulasi 🎲</h3>", unsafe_allow_html=True)
            st.dataframe(df_hasil)

        with tab_addform:      
            # Formulir untuk menambahkan data Suku Cadang baru
            st.subheader("Tambah Data Suku Cadang Baru 🔩")
            with st.expander("Tambah Data Suku Cadang Baru"):
                new_Kode_Material_suku_cadang = st.text_input("Kode Material", "", key="input_kodes_baru")
                new_NamaMaterial_suku_cadang = st.text_input("Nama Material", "", key="input_s_baru")
                new_Harga_suku_cadang = st.text_input("Harga Material", "")
                new_Biaya_suku_cadang = st.text_input("Biaya Pemesanan", "")
                new_Biaya_Penyimpanan = st.text_input("Biaya Penyimpanan", "")
                new_Biaya_Stockout = st.text_input("Biaya Stockout", "")
                new_Leadtime = st.text_input("Leadtime", "")
                new_Stok = st.text_input("Stok", "")

                # Validasi untuk memastikan tidak ada kolom yang kosong
                if st.button("Simpan Data Suku Cadang Baru"):
                    if any([new_Kode_Material_suku_cadang == "", new_NamaMaterial_suku_cadang == "", new_Harga_suku_cadang == "", new_Biaya_suku_cadang == "", new_Biaya_Penyimpanan == "", new_Biaya_Stockout == "", new_Leadtime == "", new_Stok == ""]):
                        st.warning("Semua kolom input harus diisi. Harap lengkapi formulir.")
                    else:
                        insert_query_suku_cadang = f"INSERT INTO suku_cadang (Kode_Material, Nama_Material, Harga_Material, Biaya_Pemesanan, Biaya_Penyimpanan, Biaya_Stockout, Leadtime, Stok) VALUES ('{new_Kode_Material_suku_cadang}','{new_NamaMaterial_suku_cadang}', '{new_Harga_suku_cadang}', '{new_Biaya_suku_cadang}', '{new_Biaya_Penyimpanan}', '{new_Biaya_Stockout}', '{new_Leadtime}', '{new_Stok}')"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(insert_query_suku_cadang)
                                connection.commit()
                                st.success("Data suku cadang baru berhasil disimpan!")
                            except mysql.connector.Error as e:
                                st.error(f"Error inserting data suku cadang baru: {e}")
                        
            # Formulir untuk menambahkan data supplier baru
            st.subheader("Tambah Data Supplier Baru 🏢")
            with st.expander("Tambah Data Supplier Baru"):
                new_Kode_Material = st.text_input("Kode Material", "", key="add_kodematerialsupplier_select")
                new_Nama_Material = st.text_input("Nama Material", "", key="add_namamaterialsupplier_select")
                new_ID_Supplier = st.text_input("ID Supplier", "")
                new_Nama_Supplier = st.text_input("Nama Supplier", "")
                new_Alamat_Supplier = st.text_input("Alamat Supplier", "")
                new_Contact_Supplier = st.text_input("Contact Supplier", "")
                new_Email_Contact = st.text_input("Email Contact", "")
                new_Contact_Name = st.text_input("Contact Name", "")

                # Validasi untuk memastikan tidak ada kolom yang kosong
                if st.button("Simpan Data Supplier Baru"):
                    if any([new_Kode_Material == "", new_Nama_Material=="", new_ID_Supplier == "", new_Nama_Supplier == "", new_Alamat_Supplier == "", new_Contact_Supplier == "", new_Email_Contact == "", new_Contact_Name == ""]):
                        st.warning("Semua kolom input harus diisi. Harap lengkapi formulir.")
                    else:
                        # Lakukan insert ke database sesuai dengan data yang dimasukkan
                        insert_query_supplier = f"INSERT INTO supplier (Kode_Material, Nama_Material ,ID_Supplier, Nama_Supplier, Alamat_Supplier, Contact_Supplier, Email_Contact, Contact_Name) VALUES ('{new_Kode_Material}', '{new_Nama_Material}', '{new_ID_Supplier}', '{new_Nama_Supplier}', '{new_Alamat_Supplier}', '{new_Contact_Supplier}', '{new_Email_Contact}', '{new_Contact_Name}')"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(insert_query_supplier)
                                connection.commit()
                                st.success("Data supplier baru berhasil disimpan!")
                            except mysql.connector.Error as e:
                                st.error(f"Error inserting data supplier baru: {e}")
                                
            # Formulir untuk menambahkan data permintaan
            st.subheader("Tambah Data Permintaan 📦")
            with st.expander("Tambah Data Permintaan"):
                new_Kode_Material_permintaan = st.selectbox("Kode Material", df_suku_cadang['Kode_Material'], key="input_kodepermintaan_baru")
                new_NamaMaterial_permintaan = st.selectbox("Nama Material", df_suku_cadang['Nama_Material'], key="input_namapermintaan_baru")
                new_Tahun_permintaan = st.text_input("Tahun Permintaan", "")
                new_Bulan_permintaan = st.text_input("Bulan Permintaan", "")
                new_Data_permintaan = st.text_input("Jumlah Permintaan", "")

                # Validasi untuk memastikan tidak ada kolom yang kosong
                if st.button("Simpan Data Permintaan"):
                    if any([new_Kode_Material_permintaan == "", new_NamaMaterial_permintaan == "", new_Tahun_permintaan == "", new_Bulan_permintaan == "", new_Data_permintaan == ""]):
                        st.warning("Semua kolom input harus diisi. Harap lengkapi formulir.")
                    else:
                        insert_query_permintaan = f"INSERT INTO data_permintaan (Kode_Material, Nama_Material, Tahun, Bulan, Permintaan) VALUES ('{new_Kode_Material_permintaan}','{new_NamaMaterial_permintaan}', '{new_Tahun_permintaan}', '{new_Bulan_permintaan}', '{new_Data_permintaan}')"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(insert_query_permintaan)
                                connection.commit()
                                st.success("Data permintaan berhasil disimpan!")
                            except mysql.connector.Error as e:
                                st.error(f"Error inserting data permintaan: {e}")

            # Formulir untuk menambahkan data pemesanan
            st.subheader("Tambah Data Pemesanan 📋")
            with st.expander("Tambah Data Pemesanan"):
                new_id_pemesanan = st.text_input("ID Pemesanan", "", key="input_idpemesanan_baru")
                new_idmonte_pemesanan = st.text_input("ID Simulasi", "", key="input_idmontepemesanan_baru")
                new_kode_sukucadang_pemesanan = st.selectbox("Kode Suku Cadang", df_suku_cadang['Kode_Material'])
                new_tanggal_pemesanan = st.date_input("Tanggal Permintaan", datetime.now())
                new_supplier_pemesanan = st.selectbox("ID Supplier", df_supplier["ID_Supplier"], key="input_idsup_baru")

                # Validasi untuk memastikan tidak ada kolom yang kosong
                if st.button("Simpan Data Pemesanan"):
                    if any([new_id_pemesanan == "", new_idmonte_pemesanan == "", new_kode_sukucadang_pemesanan == "", new_tanggal_pemesanan == "", new_supplier_pemesanan == ""]):
                        st.warning("Semua kolom input harus diisi. Harap lengkapi formulir.")
                    else:
                        insert_query_permintaan = f"INSERT INTO data_pemesanan (ID_Pemesanan, ID_Simulasi, Kode_Suku_Cadang, Tanggal, ID_Supplier) VALUES ('{new_id_pemesanan}','{new_idmonte_pemesanan}', '{new_kode_sukucadang_pemesanan}', '{new_tanggal_pemesanan}', '{new_supplier_pemesanan}'"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(insert_query_permintaan)
                                connection.commit()
                                st.success("Data pemesanan berhasil disimpan!")
                            except mysql.connector.Error as e:
                                st.error(f"Error inserting data pemesanan: {e}")

        with tab_editform:
            
            # Formulir untuk mengedit data Suku Cadang
            st.subheader("Edit Data Suku Cadang 🔩")
            with st.expander("Form Data Suku Cadang"):
                # Pilih pemesanan untuk diedit
                selected_suku_cadang = st.selectbox("Pilih Nama Material Suku Cadang", df_supplier['Nama_Material'], key="edit_pemesanan_select")

                # Input kolom-kolom yang dapat diedit
                edit_KodeMaterial_suku_cadang = st.text_input("Kode Material Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Kode_Material'].iloc[0], key="edit_suku_cadang_kodematerial")
                edit_NamaMaterial_suku_cadang = st.text_input("Nama Material Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Nama_Material'].iloc[0], key="edit_suku_cadang_namamaterial")
                edit_Harga_suku_cadang = st.text_input("Harga Material Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Harga_Material'].iloc[0])
                edit_Biaya_suku_cadang = st.text_input("Biaya Pemesanan Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Biaya_Pemesanan'].iloc[0])
                edit_Biaya_Penyimpanan = st.text_input("Biaya Penyimpanan Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Biaya_Penyimpanan'].iloc[0])
                edit_Biaya_Stockout = st.text_input("Biaya Stockout Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Biaya_Stockout'].iloc[0])
                edit_Leadtime = st.text_input("Leadtime Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Leadtime'].iloc[0])
                edit_Stok = st.text_input("Stok Baru", df_suku_cadang[df_supplier['Nama_Material'] == selected_suku_cadang]['Stok'].iloc[0])

                # Tombol untuk menyimpan perubahan
                if st.button("Simpan Perubahan Suku Cadang"):
                    # Lakukan update ke database sesuai dengan perubahan yang dimasukkan
                    update_query_suku_cadang = f"UPDATE suku_cadang SET Kode_Material = '{edit_KodeMaterial_suku_cadang}', Nama_Material = '{edit_NamaMaterial_suku_cadang}', Harga_Material = '{edit_Harga_suku_cadang}', Biaya_Penyimpanan = '{edit_Biaya_Penyimpanan}', Biaya_Stockout = '{edit_Biaya_Stockout}', Biaya_Pemesanan = '{edit_Biaya_suku_cadang}', Leadtime = '{edit_Leadtime}', Stok = '{edit_Stok}' WHERE Nama_Material = '{selected_suku_cadang}'"
                    with connection.cursor() as cursor:
                        try:
                            cursor.execute(update_query_suku_cadang)
                            connection.commit()
                            st.success("Perubahan data suku cadang berhasil disimpan!")
                        except mysql.connector.Error as e:
                            st.error(f"Error updating data suku cadang: {e}")
            
            # Formulir untuk mengedit data Supplier
            st.subheader("Edit Data Supplier 🏢")
            with st.expander("Form Data Supplier"):
                # Pilih supplier untuk diedit
                selected_supplier = st.selectbox("Pilih Nama Material Supplier", df_supplier['Nama_Material'], key="edit_supplier_select")

                # Input kolom-kolom yang dapat diedit
                edit_Kode_Material = st.text_input("Kode Material Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Kode_Material'].iloc[0], key="edit_supplier_kodematerial")
                edit_Nama_Material = st.text_input("Nama Material Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Nama_Material'].iloc[0], key="edit_supplier_namamaterial")
                edit_ID_Supplier = st.text_input("ID Supplier Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['ID_Supplier'].iloc[0])
                edit_Nama_Supplier = st.text_input("Nama Supplier Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Nama_Supplier'].iloc[0])
                edit_Alamat_Supplier = st.text_input("Alamat Supplier Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Alamat_Supplier'].iloc[0])
                edit_Contact_Supplier = st.text_input("Contact Person Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Contact_Supplier'].iloc[0])
                edit_Email_Contact = st.text_input("Email Contact Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Email_Contact'].iloc[0])
                edit_Contact_Name = st.text_input("Email Contact Baru", df_supplier[df_supplier['Nama_Material'] == selected_supplier]['Contact_Name'].iloc[0])

                # Tombol untuk menyimpan perubahan
                if st.button("Simpan Perubahan Supplier"):
                    # Lakukan update ke database sesuai dengan perubahan yang dimasukkan
                    update_query = f"UPDATE supplier SET Kode_Material = '{edit_Kode_Material}', Nama_Material = '{edit_Nama_Material}', Nama_Supplier = '{edit_Nama_Supplier}', ID_Supplier = '{edit_ID_Supplier}', Contact_Supplier = '{edit_Contact_Supplier}', Email_Contact = '{edit_Email_Contact}', Alamat_Supplier = '{edit_Alamat_Supplier}' , Contact_Name = '{edit_Contact_Name}' WHERE Nama_Material = '{selected_supplier}'"
                    with connection.cursor() as cursor:
                        try:
                            cursor.execute(update_query)
                            connection.commit()
                            st.success("Perubahan data supplier berhasil disimpan!")
                        except mysql.connector.Error as e:
                            st.error(f"Error updating data supplier: {e}")
                            
            # Formulir untuk mengedit data Permintaan
            st.subheader("Edit Data Permintaan 📦")
            with st.expander("Form Data Permintaan"):
                # Pilih Permintaan untuk diedit
                selected_permintaan = st.selectbox("Pilih Id Permintaan", df_permintaan['id'], key="edit_permintaan_select")
                
                # Filter DataFrame based on selected ID
                selected_row = df_permintaan[df_permintaan['id'] == selected_permintaan]

                if not selected_row.empty:
                    # Input kolom-kolom yang dapat diedit
                    edit_Kode_Material = st.text_input("Kode Material Baru", selected_row['Kode_Material'].iloc[0], key="edit_permintaan_kodematerial")
                    edit_Nama_Material = st.text_input("Nama Material Baru", selected_row['Nama_Material'].iloc[0], key="edit_permintaan_namamaterial")
                    edit_Tahun_Permintaan = st.text_input("Tahun Permintaan Baru", selected_row['Tahun'].iloc[0])
                    edit_Bulan_Permintaan = st.text_input("Bulan Permintaan Baru", selected_row['Bulan'].iloc[0])
                    edit_Jumlah_Permintaan = st.text_input("Jumlah Permintaan Baru", selected_row['Permintaan'].iloc[0])

                    # Tombol untuk menyimpan perubahan
                    if st.button("Simpan Perubahan Permintaan"):
                        # Lakukan update ke database sesuai dengan perubahan yang dimasukkan
                        update_query = f"UPDATE data_permintaan SET Kode_Material = '{edit_Kode_Material}',Nama_Material = '{edit_Nama_Material}', Tahun = '{edit_Tahun_Permintaan}', Bulan = '{edit_Bulan_Permintaan}', Permintaan = '{edit_Jumlah_Permintaan}' WHERE id = '{selected_permintaan}'"
                        
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(update_query)
                                connection.commit()
                                st.success("Perubahan data permintaan berhasil disimpan!")
                            except mysql.connector.Error as e:
                                st.error(f"Error updating data permintaan: {e}")
                else:
                    st.warning("No rows match the selected ID.")
                    
        # Formulir untuk menghapus data berdasarkan Nama Material Suku Cadang
        with tab_deleteform:
            # Fungsi untuk menghapus data berdasarkan Nama Material Suku Cadang
            st.subheader("Hapus Data Suku Cadang 🔩")
            with st.expander("Form Hapus Data Suku Cadang"):
                # Pilih suku cadang untuk dihapus
                selected_suku_cadang_to_delete_kode_material = st.selectbox("Pilih kode Material Suku Cadang", df_suku_cadang['Kode_Material'], key="delete_suku_cadang_kode_material_select")

                # Display all data for the selected kode Material
                selected_suku_cadang_data = df_suku_cadang[df_suku_cadang['Kode_Material'] == selected_suku_cadang_to_delete_kode_material]

                if not selected_suku_cadang_data.empty:
                    st.dataframe(selected_suku_cadang_data)

                    # Tombol untuk menghapus data
                    if st.button("Hapus Data Suku Cadang"):
                        # Get the ID of the selected kode Material
                        selected_suku_cadang_to_delete_id = selected_suku_cadang_data['id'].iloc[0]

                        # Lakukan delete ke database sesuai dengan data yang dipilih
                        delete_query_suku_cadang = f"DELETE FROM suku_cadang WHERE id = '{selected_suku_cadang_to_delete_id}'"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(delete_query_suku_cadang)
                                connection.commit()
                                st.success("Data suku cadang berhasil dihapus!")
                            except mysql.connector.Error as e:
                                st.error(f"Error deleting data suku cadang: {e}")
                else:
                    st.warning("No data found for the selected kode Material.")
                    
            # Fungsi untuk menghapus data supplier
            st.subheader("Hapus Data Supplier 🏢")
            with st.expander("Form Hapus Data Supplier"):
                selected_supplier_to_delete_kode_material = st.selectbox("Pilih kode Material Suku Cadang", df_supplier['Kode_Material'], key="delete_supplier_ID_select")

                # Display all data for the selected ID Supplier
                selected_supplier_data = df_supplier[df_supplier['Kode_Material'] == selected_supplier_to_delete_kode_material]

                if not selected_supplier_data.empty:
                    st.dataframe(selected_supplier_data)

                    # Tombol untuk menghapus data
                    if st.button("Hapus Data Supplier"):
                        # Get the ID of the selected kode Material
                        selected_supplier_to_delete_id = selected_supplier_data['id'].iloc[0]
                        
                        delete_query_supplier = f"DELETE FROM supplier WHERE id = '{selected_supplier_to_delete_id}'"
                        with connection.cursor() as cursor:
                            try:
                                cursor.execute(delete_query_supplier)
                                connection.commit()
                                st.success("Data supplier berhasil dihapus!")
                            except mysql.connector.Error as e:
                                st.error(f"Error deleting data supplier: {e}")
                else:
                    st.warning("No data found for the selected kode Material Supplier.")
                        
    else:
        st.error("Koneksi ke database gagal.")

# Halaman login
if not login():
    st.stop()

# Halaman admin setelah login
admin_page()
