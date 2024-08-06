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
        return None

def get_supplier_info(selected_material, connection):
    query = f"SELECT * FROM supplier WHERE Nama_Material = '{selected_material}'"
    df_sup = pd.read_sql(query, connection)
    return df_sup

# Fungsi untuk mendapatkan nilai unik berdasarkan Nama_Material
def get_unique_permintaan_by_material(selected_material, connection):
    query = f"SELECT Permintaan FROM data_permintaan WHERE Nama_Material = '{selected_material}'"
    df = pd.read_sql(query, connection)
    return df['Permintaan']

# Fungsi untuk menghitung COUNTIF
def countif(series, value):
    return series[series == value].count()

def convert_to_range(cumulative, num_ranges):
    return math.ceil(cumulative * num_ranges)

# Fungsi untuk melakukan simulasi Monte Carlo
def monte_carlo_simulation(countif_results, total_count, num_simulations):
    simulation_results = []

    for _ in range(num_simulations):
        random_value = np.random.rand()  # Generate a random value between 0 and 1
        cumulative_ratio = 0

        for value, count in countif_results.items():
            ratio = count / total_count
            cumulative_ratio += ratio

            if random_value <= cumulative_ratio:
                simulation_results.append(value)
                break

    return simulation_results

def submitted():
    st.session_state.submitted = True
def reset():
    st.session_state.submitted = False

# Main Streamlit app
def main():
    st.set_page_config(page_title="SPKPP App", page_icon="🚅", layout="centered", initial_sidebar_state="auto")
    st.sidebar.markdown("<h1 style='color: #1F2855;'>Main Menu</h1>", unsafe_allow_html=True)
    with st.container():
        # Koneksi ke database
        connection = create_connection()

        # Mendapatkan daftar unique Nama_Material dari database
        unique_materials = pd.read_sql("SELECT DISTINCT Nama_Material FROM data_permintaan", connection)['Nama_Material'].tolist()

        # Sidebar for data selection
        selected_material = st.sidebar.selectbox("**Pilih Nama Material 📦:**", unique_materials)
        # Tambahkan input tanggal awal dan akhir menggunakan widget date_input

        # Tanggal awal default (saat ini)
        default_start_date = datetime.now()

        # Tanggal akhir default (2 tahun dari tanggal awal)
        default_end_date = default_start_date + timedelta(days=365)

        # Buat input rentang waktu
        start_date = st.sidebar.date_input("Pilih Tanggal Awal", default_start_date)
        end_date = st.sidebar.date_input("Pilih Tanggal Akhir", default_end_date)
        
        submit = st.sidebar.button("Run Simulation")
        
        submit_sup = st.sidebar.button("Cek Supplier")
        
        # Cek apakah rentang waktu lebih dari 2 tahun
        if (end_date - start_date).days > 365:
            st.sidebar.warning("Rentang waktu tidak boleh melebihi 1 tahun. ⚠️")
        else:
            st.sidebar.success("Rentang waktu valid. ✅")

        unique_permintaan = get_unique_permintaan_by_material(selected_material, connection)
        st.markdown("<h1 style='text-align: center; color: #0093AD;'>Sistem Pendukung Keputusan Pengendalian Persediaan Suku Cadang (SPKPP)</h1>", unsafe_allow_html=True)

    with st.container():
        if selected_material and submit_sup or submit:
            df_supplier = get_supplier_info(selected_material, connection)
            # Display the supplier information table
            st.sidebar.write("---")
            st.sidebar.write('📦**Supplier Information:**')
            for index, row in df_supplier.iterrows():
                st.sidebar.write(f"**Kode Material:** {row['Kode_Material']}")
                st.sidebar.write(f"**Nama Material:** {row['Nama_Material']}")
                st.sidebar.write(f"**Supplier ID:** {row['ID_Supplier']}")
                st.sidebar.write(f"**Nama Supplier:** {row['Nama_Supplier']}")
                st.sidebar.write(f"**Alamat Supplier:** {row['Alamat_Supplier']}")
                st.sidebar.write(f"**Contact Supplier:** {row['Contact_Supplier']}")
                st.sidebar.write(f"**Contact Nama:** {row['Contact_Name']}")
                st.sidebar.write(f"**Email Contact:** {row['Email_Contact']}")
                st.sidebar.write("---")
                
        if selected_material and submit:
            with st.container():
                tab_montecarlo, tab_cr, tab_kebijakan, tab_keputusan = st.tabs(["Peramalan Kebutuhan SKCD (Monte Carlo)", "Parameter s, Q", "Skenario Pengendalian", "Keputusan Pengendalian"])
                
                with tab_montecarlo:
                    st.markdown("<h2 style='color: #1F2855;'>Probabilitas Frekuensi Penyerapan</h2>", unsafe_allow_html=True)
                    st.write("Ini adalah konten hasil Frekuensi Penyerapan.")
                    col1, col2 = st.columns([3,6])
                    # Menampilkan hasil analisis data
                    with col1:

                        st.write(f"Nilai Unik Permintaan untuk {selected_material}:")
                        # Menghitung COUNTIF untuk setiap nilai unik
                        countif_results = {}
                        for value in unique_permintaan.unique():
                            count = countif(unique_permintaan, value)
                            st.write(f"{value}: {count}")
                            countif_results[value] = count

                        # Jumlahkan hasil COUNTIF
                        total_count = sum(countif_results.values())
                        st.write(f"Total: {total_count}")
                    with col2:
                        # Bagi COUNTIF individu dengan total COUNTIF
                        st.write("COUNTIF / Total COUNTIF:")
                        cumulative_ratio = 0
                        num_ranges = 101  # Jumlah rentang yang diinginkan
                        for value, count in countif_results.items():
                            ratio = count / total_count
                            cumulative_ratio += ratio
                            range_start = convert_to_range(cumulative_ratio - ratio, num_ranges)
                            range_end = convert_to_range(cumulative_ratio, num_ranges) - 1
                            st.write(f"{value}: {count} / {total_count} = {ratio:.2%} (Kumulatif: {cumulative_ratio:.2%}) (Range: {range_start} hingga {range_end})")
                    
                    st.markdown("<h2 style='color:#F26924;'>Simulasi Monte Carlo</h2>", unsafe_allow_html=True)
                    # Simulasi Monte Carlo
                    num_simulations = 12
                    st.write(f"\nSimulasi Monte Carlo ({num_simulations} simulasi):")
                    simulation_results_table = pd.DataFrame()
                    col1, col2 = st.columns([3,3])
                    all_simulation_results = []

                    for set_index in range(5):
                        simulation_results = monte_carlo_simulation(countif_results, total_count, num_simulations)
                        simulation_results_table[f'Set {set_index + 1}'] = simulation_results
                        all_simulation_results.append(simulation_results)

                    with col1:
                        st.write("Hasil Simulasi:")
                        st.write(simulation_results_table)

                        # Hitung dan tampilkan rata-rata dari hasil simulasi
                        average_result = np.mean(all_simulation_results, axis=1)
                        st.write("\nRata-rata Hasil Simulasi:")
                        for i, column in enumerate(simulation_results_table.columns):
                            st.write(f"{column} (Average): {average_result[i]:.2f}")

                        # Hitung dan tampilkan standar deviasi dari hasil simulasi
                        std_dev = np.std(average_result)
                        st.write("\nStandar Deviasi Hasil Simulasi:")
                        st.write(f"Std Dev: {std_dev:.2f}")

                        # Hitung dan tampilkan half-width (HW)
                        num_replications = len(all_simulation_results)
                        hw = (2.776 * std_dev) / np.sqrt(num_replications)
                        st.write(f"\nHalf-Width (HW): {hw:.2f}")

                        # Hitung dan tampilkan sample size adjustment (n')
                        n_prime = ((1.96 * std_dev) / hw)**2
                        rounded_n_prime = math.ceil(n_prime)
                        st.write(f"\nSample Size Adjustment (n'): {n_prime:.5f}")
                        st.write(f"\nMinimal Replikasi (N Akhir): {rounded_n_prime}")
                    
                    with col2:
                        # Buat tabel baru untuk satu set dengan data yang diminta
                        set_average_rounded = np.round(np.mean(all_simulation_results, axis=0)).astype(int)
                        set_average_table = pd.DataFrame({'Nilai_Random': set_average_rounded})
                        st.write("\nTabel Set Rata-rata Bulat:")
                        st.write(set_average_table)

                        # Hitung dan tampilkan total dan standar deviasi dari rounded averages
                        total_rounded_average = np.sum(set_average_rounded)
                        std_dev_rounded_average = np.std(set_average_rounded)
                        st.write(f"\nTotal Rounded Average: {total_rounded_average}")
                        st.write(f"Standar Deviasi Rounded Average: {std_dev_rounded_average:.2f}")
            
                with tab_cr:
                    st.markdown("<h2 style='color: #0093AD;'>CR (s,Q)</h2>", unsafe_allow_html=True)

                    # Fungsi Ambil data kolom Biaya_Pemesanan, Biaya_Penyimpanan, Biaya_Stockout, dan Leadtime berdasarkan Nama_Material
                    def pemesanan_data(selected_material, connection):
                        query = f"SELECT Harga_Material, Biaya_Pemesanan, Biaya_Penyimpanan, Biaya_Stockout, Leadtime FROM suku_cadang WHERE Nama_Material = '{selected_material}'"
                        df_pemesanan = pd.read_sql(query, connection)
                        return df_pemesanan
                    
                    biaya_pemesanan_data = pemesanan_data(selected_material, connection)
                    
                    # Tampilkan data biaya_pemesanan
                    st.write("\nData Suku Cadang:")
                    st.write(biaya_pemesanan_data)
                    
                    # Bagi Leadtime dengan 52
                    pembagian_leadtime = biaya_pemesanan_data['Leadtime']/52

                    # Tampilkan data setelah Leadtime dibagi 52
                    st.write("Data Suku Cadang setelah Leadtime dibagi 52:", pembagian_leadtime)

                    # Hitung dan tampilkan hasil pembagian (Step 1)
                    step1_result = np.ceil(pembagian_leadtime * total_rounded_average)
                    st.write("Hasil Pembagian (Step 1):", step1_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 2)
                    step2_result = np.ceil(std_dev_rounded_average * np.sqrt(pembagian_leadtime))
                    st.write("Hasil Perhitungan (Step 2):", step2_result)
                    
                    # Ambil data Biaya_Pemesanan dan Biaya_Penyimpanan
                    biaya_pemesanan_penyimpanan_data = biaya_pemesanan_data[['Biaya_Pemesanan', 'Biaya_Penyimpanan', 'Biaya_Stockout']]

                    # Hitung dan tampilkan hasil perhitungan (Step 3a)
                    step3a_result = np.ceil(np.sqrt((2 * biaya_pemesanan_penyimpanan_data['Biaya_Pemesanan'] * total_rounded_average) / biaya_pemesanan_penyimpanan_data['Biaya_Penyimpanan']))
                    st.write("Hasil Perhitungan (Step 3a):", step3a_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 3b)
                    step3b_result = 1 - ((biaya_pemesanan_penyimpanan_data['Biaya_Penyimpanan'] * step3a_result) / (biaya_pemesanan_penyimpanan_data['Biaya_Stockout'] * total_rounded_average))
                    st.write("Hasil Perhitungan (Step 3b):", step3b_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 3c)
                    step3c_result = np.ceil(step1_result + (step3b_result * step2_result))
                    st.write("Hasil Perhitungan (Step 3c):", step3c_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 3d)
                    norm_cdf_step3b = stats.norm.cdf(step3b_result)
                    step3d_result = step2_result * norm_cdf_step3b
                    st.write("Hasil Perhitungan (Step 3d):", step3d_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 4)
                    step4_result = np.ceil(np.sqrt((2 * total_rounded_average * (biaya_pemesanan_penyimpanan_data['Biaya_Pemesanan'] + (biaya_pemesanan_penyimpanan_data['Biaya_Stockout'] * step3d_result))) / biaya_pemesanan_penyimpanan_data['Biaya_Penyimpanan']))
                    st.write("Hasil Perhitungan (Step 4):", step4_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 3b_2)
                    step3b_2_result = 1 - ((biaya_pemesanan_penyimpanan_data['Biaya_Penyimpanan'] * step4_result) / (biaya_pemesanan_penyimpanan_data['Biaya_Stockout'] * total_rounded_average))
                    st.write("Hasil Perhitungan (Step 3b_2):", step3b_2_result)
                    
                    # Hitung dan tampilkan hasil perhitungan (Step 3c_2)
                    step3c_2_result = np.ceil(step1_result + (step3b_2_result * step2_result))
                    st.write("Hasil Perhitungan (Step 3c_2):", step3c_2_result)
                    
                    # Buat tabel sesuai dengan spesifikasi
                    iterasi_values = ['Q', 's']
                    iterasi_column = pd.Series(iterasi_values, name='Iterasi')

                    table_data = {
                        '0': [step3a_result, step3c_result],
                        '1': [step4_result, step3c_2_result]
                    }

                    result_table = pd.DataFrame(table_data, index=iterasi_column)

                    # Format the DataFrame before displaying it
                    formatted_table = result_table.applymap(lambda x: f"{int(x):,}")

                    # Display the formatted table
                    st.write("\nTabel Hasil Perhitungan:")
                    st.table(formatted_table)
                    
                    # Fungsi untuk mendapatkan nilai stok berdasarkan Nama_Material
                    def suku_cadang_data(selected_material, connection):
                        query = f"SELECT Stok FROM suku_cadang WHERE Nama_Material = '{selected_material}'"
                        df = pd.read_sql(query, connection)
                        return df
                    
                    # Fetch leadtime from the database for the selected_material
                    cursor = connection.cursor()
                    leadtime_query = f"SELECT Leadtime FROM suku_cadang WHERE Nama_Material = '{selected_material}'"
                    cursor.execute(leadtime_query)
                    leadtime_result = cursor.fetchone()
                    cursor.close()

                    leadtime = round(leadtime_result[0]) if leadtime_result else 0

                    # Assuming set_average_table is available
                    set_average_rounded = set_average_table['Nilai_Random'].values.astype(int)

                with tab_kebijakan:
                    col1, col2 = st.columns([3,3], gap="large")
                    with col1 :
                        # Fungsi Kebijakan CR (s,Q)
                        def initialize_month_dataframe(selected_material, connection, set_average_rounded):
                            # Generate data for 1 year (2024)
                            start_date = datetime(2024, 1, 1)
                            end_date = datetime(2024, 12, 31)
                            date_range = pd.date_range(start_date, end_date)

                            # Create an empty DataFrame
                            data = pd.DataFrame(index=date_range, columns=['Stok Awal', 'Permintaan', 'Received', 'Stok Akhir', 'Order', 'Backorder', 's', 'Q'])

                            # Fill the DataFrame with initial values
                            stok_awal = suku_cadang_data(selected_material, connection)
                            if not stok_awal.empty:
                                # Convert to float (if needed)
                                stok_awal = stok_awal.astype(float)

                                # Set 'Stok Awal' using the last available value from the database
                                last_available_stok = stok_awal.iloc[-1]['Stok']
                                data['Stok Awal'] = last_available_stok

                            # Set nilai permintaan pada setiap tanggal 1
                            data.loc[data.index.day == 1, 'Permintaan'] = set_average_rounded

                            # Fill 'Received' with 0 if missing
                            data['Received'].fillna(0, inplace=True)
                            data['Permintaan'].fillna(0, inplace=True)
                            data.loc[date_range[0],'s'] = step3c_2_result.values[0]
                            data.loc[date_range[0],'Q'] = step4_result.values[0]
                            
                            # Calculate Backorder ensuring it is the positive difference between demand and available stock
                            data.loc[date_range[0], 'Backorder'] = max(0, data.loc[date_range[0], 'Permintaan'] - data.loc[date_range[0], 'Stok Awal'])
                            
                            # Initialize 'Stok Akhir' pada baris pertama
                            data.loc[date_range[0], 'Stok Akhir'] = data.loc[date_range[0], 'Stok Awal'] - data.loc[date_range[0], 'Permintaan'] + data.loc[date_range[0], 'Received']
                            # Calculate Order on January 1st
                            if data.loc[date_range[0], 'Stok Akhir'] <= data.loc[date_range[0], 's']:
                                data.loc[date_range[0], 'Order'] = data.loc[date_range[0], 'Q']
                                # Mengisi Received dengan nilai Order pada leadtime * 7                      
                                leadtime_days = round(leadtime * 7)
                                received_date = date_range[0] + pd.DateOffset(days=leadtime_days)
                                data.loc[received_date, 'Received'] = data.loc[date_range[0], 'Order']
                                data.loc[received_date, 'Stok Akhir'] += data.loc[received_date, 'Received'] - data.loc[date_range[0], 'Permintaan']
                            else:
                                data.loc[date_range[0], 'Order'] = 0
                            
                            # Calculate Stok Awal pada tanggal 1 Januari dan Stok Akhir, Order, dan Backorder untuk tanggal lainnya
                            for i in range(1, len(date_range)):
                                
                                data.loc[date_range[i],'s'] = step3c_2_result.values[0]
                                data.loc[date_range[i],'Q'] = step4_result.values[0]
                                
                                # Isi 'Stok Awal' hanya pada tanggal 1 Januari
                                if date_range[i].day == 1:
                                    data.loc[date_range[i], 'Stok Awal'] = data.loc[date_range[i - 1], 'Stok Akhir']
                                else:
                                    # Ambil nilai 'Stok Akhir' untuk tanggal setelah 1 Januari
                                    data.loc[date_range[i], 'Stok Awal'] = data.loc[date_range[i - 1], 'Stok Akhir']

                                # Hitung Stok Akhir, Order, dan Backorder
                                if pd.isna(data.loc[date_range[i], 'Permintaan']) or data.loc[date_range[i], 'Permintaan'] == 0:
                                    # Jika Permintaan NaN atau 0, ambil nilai dari hari sebelumnya
                                    data.loc[date_range[i], ['Stok Akhir', 'Order', 'Backorder']] = data.loc[date_range[i - 1], ['Stok Akhir', 'Order', 'Backorder']]
                                else:
                                    # Jika Permintaan tidak NaN dan tidak 0, hitung normal
                                    data.loc[date_range[i], 'Stok Akhir'] = data.loc[date_range[i - 1], 'Stok Akhir'] - data.loc[date_range[i], 'Permintaan'] + data.loc[date_range[i], 'Received']
                                    data.loc[date_range[i], 'Order'] = 0

                                # Calculate Backorder ensuring it is the positive difference between demand and available stock
                                data.loc[date_range[i], 'Backorder'] = max(0, data.loc[date_range[i], 'Permintaan'] - data.loc[date_range[i], 'Stok Awal'])

                                # Menghitung Order pada tanggal 1 setelah Januari                       
                                leadtime_days = round(leadtime * 7)
                                received_date = date_range[i] + pd.DateOffset(days=leadtime_days)
                                                                # Di akhir loop, lakukan kumulatif Received ke Stok Akhir pada tanggal yang sama
                                data.loc[date_range[i], 'Stok Akhir'] += data.loc[date_range[i], 'Received']

                                if data.loc[date_range[i], 'Permintaan'] > 0 and data.loc[date_range[i], 'Stok Akhir'] <= data.loc[date_range[i],'s'] or data.loc[date_range[i], 'Received'] > 0 and data.loc[date_range[i], 'Stok Akhir'] <= data.loc[date_range[i],'s']:
                                    data.loc[date_range[i], 'Order'] = data.loc[date_range[i],'Q']

                                    # Mengisi Received dengan nilai Order pada leadtime * 7
                                    if data.loc[date_range[i], 'Order'] > 0:
                                        data.loc[received_date, 'Received'] = data.loc[date_range[i],'Q']
                                        data.loc[date_range[i], 'Stok Akhir'] += data.loc[date_range[i], 'Received'] - data.loc[date_range[i], 'Permintaan']
                                    else:
                                        data.loc[received_date, 'Received'] = 0
                                else:
                                    data.loc[date_range[i], 'Order'] = 0
                                    
                            return data

                        data1 = initialize_month_dataframe(selected_material, connection, set_average_rounded)
                        print(data1)
                        # Display the resulting combined DataFrame
                        st.markdown("<h2 style='color:#1F2855;'>Kebijakan CR(s,Q)</h2>", unsafe_allow_html=True)
                        st.write(data1)
                        
                        # Sum the demand, order, and backorder for each month
                        total_demand = data1['Permintaan'].sum()
                        total_order = data1['Order'].sum()
                        # Menambahkan kolom 'Total Backorder' untuk menyimpan nilai backorder hanya pada tanggal akhir bulan
                        data1['Total Backorder'] = 0

                        # Menghitung Total Backorder pada tanggal akhir bulan
                        data1.loc[data1.index.is_month_start, 'Total Backorder'] = data1['Backorder']

                        # Menghitung total backorder dengan menjumlahkan nilai pada tanggal akhir bulan
                        total_backorder = data1['Total Backorder'].sum()

                        # Menghapus kolom 'Total Backorder' jika tidak dibutuhkan lagi
                        data1.drop(columns=['Total Backorder'], inplace=True)

                        # Display the totals
                        st.write("Total Demand:", total_demand)
                        st.write("Total Order:", total_order)
                        st.write("Total Backorder:", total_backorder)
                        
                        # Fetch the Harga_Material from biaya_pemesanan based on selected_material
                        harga_material = biaya_pemesanan_data['Harga_Material'].iloc[0]

                        # Calculate total cost
                        total_demand = data1['Permintaan'].sum()
                        total_cost = total_demand * harga_material

                        # Display the result
                        # Set the locale to Indonesian (Rupiah)
                        locale.setlocale(locale.LC_ALL, 'id_ID')
                        # Format total_cost as Rupiah
                        formatted_total_cost = locale.currency(total_cost, grouping=True)
                        st.write(f"Total Cost for {selected_material}: {formatted_total_cost}")
                    
                        biaya_penyimpanan = biaya_pemesanan_data['Biaya_Penyimpanan'].iloc[0]
                        biaya_stockout = biaya_pemesanan_data['Biaya_Stockout'].iloc[0]
                        biaya_pemesanan = biaya_pemesanan_data['Biaya_Pemesanan'].iloc[0]
                        
                        # Ensure 'Tanggal' is a datetime type
                        data1.index = pd.to_datetime(data1.index)
                        
                        # Calculate holding cost at the end of the year for data1
                        stok_akhir_end_of_year = data1.loc[data1.index.month == 12, 'Stok Akhir'].iloc[0]
                        holding_cost = stok_akhir_end_of_year * biaya_penyimpanan
                        
                        # Calculate holding cost at the end of the year
                        stok_akhir_end_of_year = data1.loc[data1.index.month == 12, 'Stok Akhir'].iloc[0]
                        holding_cost = stok_akhir_end_of_year * biaya_penyimpanan

                        # Format holding_cost as Rupiah
                        formatted_holding_cost = locale.currency(holding_cost, grouping=True)

                        backorder_cost = total_backorder * biaya_stockout

                        # Format holding_cost as Rupiah
                        formatted_backorder_cost = locale.currency(backorder_cost, grouping=True)
                        
                        # Filter the DataFrame for the selected material and the year
                        filtered_df = data1[(data1.index.year == 2024) & (data1['Order'] > 0)]

                        # Calculate the count of orders and the total cost
                        order_count = filtered_df['Order'].count()
                        total_order_cost = order_count * biaya_pemesanan

                        # Format total_order_cost as Rupiah
                        formatted_total_order_cost = locale.currency(total_order_cost, grouping=True)

                        # Display the result
                        st.write(f"Holding Cost at the End of the Year for {selected_material}: {formatted_holding_cost}")
                        
                        st.write(f"Backorder Cost at the End of the Year for {selected_material}: {formatted_backorder_cost}")
                        
                        # Display the result
                        st.write(f"Total Order Cost for {selected_material} in 2024: {formatted_total_order_cost}")
                        
                        #Sum
                        sum_all = total_cost + holding_cost + backorder_cost + total_order_cost
                        formatted_sum_all = locale.currency(sum_all, grouping=True)
                        # Display the result
                        st.write(f"Total All Cost {selected_material} in 2024: {formatted_sum_all}")

                        # Calculate the ratio
                        ratio = (total_demand - total_backorder) / total_demand

                        # Display the result
                        st.write(f"Ratio of (Total Permintaan - Total Backorder) / Total Permintaan: {ratio:.2%}")
                        
                    with col2:
                        st.markdown("<h2 style='color:#F26924;'>Kebijakan Perusahaan</h2>", unsafe_allow_html=True)
                        # Fungsi untuk menghasilkan data
                        def generate_data(selected_material, connection, set_average_rounded):
                            # Generate datetime
                            date_range = pd.date_range(start_date, end_date)

                            # Create an empty DataFrame
                            data = pd.DataFrame(index=date_range, columns=['Stok Awal', 'Permintaan', 'Received', 'Stok Akhir', 'Order', 'Backorder'])

                            # Fill the DataFrame with initial values
                            stok_awal_values = suku_cadang_data(selected_material, connection)
                            if not stok_awal_values.empty:
                                # Convert to float (if needed)
                                stok_awal_values = stok_awal_values.astype(float)

                                # Set 'Stok Awal' using the last available value from the database
                                last_available_stok = stok_awal_values.iloc[-1]['Stok']
                                data['Stok Awal'] = last_available_stok

                            # Set nilai permintaan pada setiap tanggal 1
                            data.loc[data.index.day == 1, 'Permintaan'] = set_average_rounded

                            # Fill 'Received' with 0 if missing
                            data['Received'].fillna(0, inplace=True)
                            data['Backorder'].fillna(0, inplace=True)
                            data['Order'].fillna(0, inplace=True)
                            data['Permintaan'].fillna(0, inplace=True)

                            # Initialize 'Stok Akhir' pada baris pertama
                            data.loc[date_range[0], 'Stok Akhir'] = data.loc[date_range[0], 'Stok Awal'] - data.loc[date_range[0], 'Permintaan'] + data.loc[date_range[0], 'Received']
                                        
                            # Calculate Stok Awal pada tanggal 1 Januari dan Stok Akhir, Order, dan Backorder untuk tanggal lainnya
                            for i in range(1, len(date_range)):
                                # Isi 'Stok Awal' hanya pada tanggal 1 Januari
                                if date_range[i].day == 1:
                                    data.loc[date_range[i], 'Stok Awal'] = data.loc[date_range[i - 1], 'Stok Akhir']
                                else:
                                    # Ambil nilai 'Stok Akhir' untuk tanggal setelah 1 Januari
                                    data.loc[date_range[i], 'Stok Awal'] = data.loc[date_range[i - 1], 'Stok Akhir']

                                # Hitung Stok Akhir, Order, dan Backorder
                                if pd.isna(data.loc[date_range[i], 'Permintaan']) or data.loc[date_range[i], 'Permintaan'] == 0:
                                    # Jika Permintaan NaN atau 0, ambil nilai dari hari sebelumnya
                                    data.loc[date_range[i], ['Stok Akhir', 'Order', 'Backorder']] = data.loc[date_range[i - 1], ['Stok Akhir', 'Order', 'Backorder']]
                                else:
                                    # Jika Permintaan tidak NaN dan tidak 0, hitung normal
                                    data.loc[date_range[i], 'Stok Akhir'] = data.loc[date_range[i - 1], 'Stok Akhir'] - data.loc[date_range[i], 'Permintaan'] + data.loc[date_range[i], 'Received']
                                    data.loc[date_range[i], 'Order'] = 0

                                # Calculate Backorder ensuring it is the positive difference between demand and available stock
                                data.loc[date_range[i], 'Backorder'] = max(0, data.loc[date_range[i], 'Permintaan'] - data.loc[date_range[i], 'Stok Awal'])

                                # Menghitung Order pada tanggal 15 April
                                if date_range[i].day == 15 and date_range[i].month == 4:
                                    backorder_next_month = data.loc[date_range[i], 'Backorder']
                                    permintaan_1 = set_average_rounded[4]  # Permintaan pada baris 5
                                    permintaan_2 = set_average_rounded[5]  # Permintaan pada baris 6
                                    permintaan_3 = set_average_rounded[6]  # Permintaan pada baris 7
                                    order_value = round((max(backorder_next_month, permintaan_1) + permintaan_2 + permintaan_3) * 1.05)
                                    data.loc[date_range[i], 'Order'] = max(0, order_value)

                                    # Mengisi Received dengan nilai Order pada leadtime * 7 setelah tanggal 15
                                    leadtime_days = round(leadtime * 7)
                                    received_date = date_range[i] + pd.DateOffset(days=leadtime_days)
                                    if data.loc[date_range[i], 'Order'] > 0:
                                        data.loc[received_date, 'Received'] = data.loc[date_range[i], 'Order']
                                        data.loc[received_date, 'Stok Akhir'] = data.loc[received_date, 'Stok Akhir'] + data.loc[received_date, 'Received'] - data.loc[date_range[i], 'Permintaan']
                                    else:
                                        data.loc[received_date, 'Received'] = 0

                                # Menghitung Order pada tanggal 15 Juli
                                elif date_range[i].day == 15 and date_range[i].month == 7:
                                    backorder_next_month = data.loc[date_range[i], 'Backorder']
                                    permintaan_1 = set_average_rounded[7]  # Permintaan pada baris 8
                                    permintaan_2 = set_average_rounded[8]  # Permintaan pada baris 9
                                    permintaan_3 = set_average_rounded[9]  # Permintaan pada baris 10
                                    order_value = round((max(backorder_next_month, permintaan_1) + permintaan_2 + permintaan_3) * 1.05)
                                    data.loc[date_range[i], 'Order'] = max(0, order_value)
                                    
                                    # Mengisi Received dengan nilai Order pada leadtime * 7 setelah tanggal 15
                                    leadtime_days = round(leadtime * 7)
                                    received_date = date_range[i] + pd.DateOffset(days=leadtime_days)
                                    if data.loc[date_range[i], 'Order'] > 0:
                                        data.loc[received_date, 'Received'] = data.loc[date_range[i], 'Order']
                                        data.loc[received_date, 'Stok Akhir'] = data.loc[received_date, 'Stok Akhir'] + data.loc[received_date, 'Received'] - data.loc[date_range[i], 'Permintaan']
                                    else:
                                        data.loc[received_date, 'Received'] = 0
                                        
                                # Menghitung Order pada tanggal 15 Oktober
                                elif date_range[i].day == 15 and date_range[i].month == 10:
                                    backorder_next_month = data.loc[date_range[i], 'Backorder']
                                    permintaan_1 = set_average_rounded[10]  # Permintaan pada baris 11
                                    permintaan_2 = set_average_rounded[11]  # Permintaan pada baris 12
                                    order_value = round((max(backorder_next_month, permintaan_1) + permintaan_2) * 1.05)
                                    data.loc[date_range[i], 'Order'] = max(0, order_value)
                                    
                                    # Mengisi Received dengan nilai Order pada leadtime * 7 setelah tanggal 15
                                    leadtime_days = round(leadtime * 7)
                                    received_date = date_range[i] + pd.DateOffset(days=leadtime_days)
                                    if data.loc[date_range[i], 'Order'] > 0:
                                        data.loc[received_date, 'Received'] = data.loc[date_range[i], 'Order']
                                        data.loc[received_date, 'Stok Akhir'] = data.loc[received_date, 'Stok Akhir'] + data.loc[received_date, 'Received'] - data.loc[date_range[i], 'Permintaan']
                                    else:
                                        data.loc[received_date, 'Received'] = 0

                                else:
                                    data.loc[date_range[i], 'Order'] = 0
                                    
                                # Di akhir loop, lakukan kumulatif Received ke Stok Akhir pada tanggal yang sama
                                data.loc[date_range[i], 'Stok Akhir'] += data.loc[date_range[i], 'Received']

                            return data

                        data = generate_data(selected_material, connection, set_average_rounded)
                        st.write(data)
                        
                        # Total Permintaan
                        total_demand_data = data['Permintaan'].sum()

                        # Total Order
                        total_order_data = data['Order'].sum()

                        # Menambahkan kolom 'Total Backorder' untuk menyimpan nilai backorder hanya pada tanggal akhir bulan
                        data['Total Backorder'] = 0

                        # Menghitung Total Backorder pada tanggal akhir bulan
                        data.loc[data.index.is_month_start, 'Total Backorder'] = data['Backorder']

                        # Menghitung total backorder dengan menjumlahkan nilai pada tanggal akhir bulan
                        total_backorder_data = data['Total Backorder'].sum()

                        # Menghapus kolom 'Total Backorder' jika tidak dibutuhkan lagi
                        data.drop(columns=['Total Backorder'], inplace=True)

                        # Display the totals
                        st.write("Total Demand (Data):", total_demand_data)
                        st.write("Total Order (Data):", total_order_data)
                        st.write("Total Backorder (Data):", total_backorder_data)

                        # Fetch the Harga_Material from biaya_pemesanan based on selected_material
                        harga_material = biaya_pemesanan_data['Harga_Material'].iloc[0]

                        # Calculate total cost for data
                        total_cost_data = total_demand_data * harga_material

                        # Display the result for data
                        # Set the locale to Indonesian (Rupiah)
                        locale.setlocale(locale.LC_ALL, 'id_ID')
                        # Format total_cost_data as Rupiah
                        formatted_total_cost_data = locale.currency(total_cost_data, grouping=True)
                        st.write(f"Total Cost for {selected_material} (Data): {formatted_total_cost_data}")
                        
                        biaya_penyimpanan_data = biaya_pemesanan_data['Biaya_Penyimpanan'].iloc[0]
                        biaya_stockout_data = biaya_pemesanan_data['Biaya_Stockout'].iloc[0]
                        biaya_pemesanan_data = biaya_pemesanan_data['Biaya_Pemesanan'].iloc[0]

                        # Ensure 'Tanggal' is a datetime type
                        data.index = pd.to_datetime(data.index)

                        # Calculate holding cost at the end of the year for data
                        stok_akhir_end_of_year_data = data.loc[data.index.month == 12, 'Stok Akhir'].iloc[0]
                        holding_cost_data = stok_akhir_end_of_year_data * biaya_penyimpanan_data

                        # Format holding_cost_data as Rupiah
                        formatted_holding_cost_data = locale.currency(holding_cost_data, grouping=True)

                        backorder_cost_data = total_backorder_data * biaya_stockout_data

                        # Format holding_cost_data as Rupiah
                        formatted_backorder_cost_data = locale.currency(backorder_cost_data, grouping=True)

                        # Filter the DataFrame for the selected material and the year for data
                        filtered_data = data[(data.index.year == 2024) & (data['Order'] > 0)]

                        # Calculate the count of orders and the total cost for data
                        order_count_data = filtered_data['Order'].count()
                        total_order_cost_data = order_count_data * biaya_pemesanan_data

                        # Format total_order_cost_data as Rupiah
                        formatted_total_order_cost_data = locale.currency(total_order_cost_data, grouping=True)

                        # Display the result for data
                        st.write(f"Holding Cost at the End of the Year for {selected_material} (Data): {formatted_holding_cost_data}")
                        st.write(f"Backorder Cost at the End of the Year for {selected_material} (Data): {formatted_backorder_cost_data}")
                        st.write(f"Total Order Cost for {selected_material} in 2024 (Data): {formatted_total_order_cost_data}")

                        # Sum for data
                        sum_all_data = total_cost_data + holding_cost_data + backorder_cost_data + total_order_cost_data
                        formatted_sum_all_data = locale.currency(sum_all_data, grouping=True)
                        # Display the result for data
                        st.write(f"Total All Cost {selected_material} in 2024 (Data): {formatted_sum_all_data}")

                        # Calculate the ratio for data
                        ratio_data = (total_demand_data - total_backorder_data) / total_demand_data

                        # Display the result for data
                        st.write(f"Ratio of (Total Permintaan - Total Backorder) / Total Permintaan (Data): {ratio_data:.2%}")
                    
                with tab_keputusan:
                
                    kepentingan_krit_total_biaya = 4.5/(4.5+5)
                    kepentingan_krit_service_level = 5/(4.5+5)
                        
                    def perbandingan_nilai(sum_all, sum_all_data):
                        if sum_all > sum_all_data:
                            return sum_all_data
                        else:
                            return sum_all
                    def perbandingan_ratio(ratio, ratio_data):
                        if ratio > ratio_data:
                            return ratio
                        else:
                            return ratio_data
                    hasil1 = perbandingan_nilai(sum_all, sum_all_data)
                    hasil2 = perbandingan_ratio(ratio, ratio_data)
                        
                    #Menghitung Normalisasi Perusahaan
                    normalisasiperusahaan_cost = sum_all_data / hasil1
                    normalisasiperusahaan_service = ratio_data / hasil2
                        
                    #Menghitung Normalisasi CR(s,Q)
                    normalisasiCR_cost = sum_all / hasil1
                    normalisasiCR_service = ratio / hasil2
                        
                    kriteria_perusahaan = (normalisasiperusahaan_cost * kepentingan_krit_total_biaya)+(normalisasiperusahaan_service * kepentingan_krit_service_level)
                    kriteria_CR = (normalisasiCR_cost * kepentingan_krit_total_biaya)+(normalisasiCR_service * kepentingan_krit_service_level)
                        
                    def perbandingan_kebijakan(kriteria_perusahaan, kriteria_CR, formatted_sum_all_data, ratio_data, formatted_sum_all, ratio):
                        if kriteria_perusahaan > kriteria_CR:
                            hasil_perbandingan = "Perusahaan"
                            total_biaya_lebih_baik = formatted_sum_all_data
                            total_service_lebih_baik = ratio_data
                        else:
                            hasil_perbandingan = "CR(s,Q)"
                            total_biaya_lebih_baik = formatted_sum_all
                            total_service_lebih_baik = ratio
                            
                        return hasil_perbandingan, total_biaya_lebih_baik, total_service_lebih_baik

                    hasil_perbandingan, total_biaya_lebih_baik, total_service_lebih_baik = perbandingan_kebijakan(kriteria_perusahaan, kriteria_CR, formatted_sum_all_data, normalisasiperusahaan_service, formatted_sum_all, normalisasiCR_service)
                                                
                    st.write('Kepentingan Krit Total Biaya', kepentingan_krit_total_biaya)
                    st.write('Kepentingan Krit Service Level', kepentingan_krit_service_level)
                    st.write(f'Min/Max: {hasil1} {hasil2:.2%}')
                    st.write(f'Normalisasi Kebijakan Perusahaan: Cost {normalisasiperusahaan_cost} | Service {normalisasiperusahaan_service}')
                    st.write(f'Normalisasi Kebijakan CR: Cost {normalisasiCR_cost} | Service {normalisasiCR_service}')
                    st.header(f'Hasil Penilaian Kriteria')
                    st.write(f'Perusahaan: {kriteria_perusahaan}')
                    st.write(f'CR: {kriteria_CR}')
                    st.header("KEPUTUSAN :")
                    st.write(f"Jumlah permintaan dan pemesanan **{selected_material}** yang optimal berdasarkan nilai Service Level dan Total Biaya yang terbaik adalah menggunakan skenario **Kebijakan {hasil_perbandingan}** dengan **Total Biaya sebesar {total_biaya_lebih_baik}** dan **Service Level sebesar {total_service_lebih_baik:.2%}**")
                    
                    # Add a button to submit the results
                    st.button("Submit Results to Database", on_click=submitted)
                    if 'submitted' in st.session_state:
                        if st.session_state.submitted == True:
                            print("Submit button pressed")
                            # Insert the results into the database
                            insert_query = f"INSERT INTO hasil_simulasi (Kode_Material, Hasil_Perbandingan, Total_Cost, Total_Service) VALUES ('{selected_material}', '{hasil_perbandingan}', '{total_biaya_lebih_baik}', '{total_service_lebih_baik}')"
                            with connection.cursor() as cursor:
                                try:
                                    cursor.execute(insert_query)
                                    connection.commit()
                                    st.sidebar.success("Results successfully submitted to the database!")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            reset() # Prevents rerunning new user creation on next page load
                            
            # Tutup koneksi database
            connection.close()

# Menjalankan aplikasi Streamlit
if __name__ == "__main__":
    main()