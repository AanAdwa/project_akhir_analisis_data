import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import streamlit as st

def create_byhour(df):
     byhour_df = df.groupby('hr').agg({
          'cnt': 'mean',
          'registered': 'mean',
          'casual': 'mean'
     }).reset_index()

     byhour_df.rename(columns={
          'hr': 'hour',
          'cnt': 'avg_total_user',
          'registered': 'avg_registered_user',
          'casual': 'avg_casual_user'
     },inplace=True)

     return byhour_df

def create_byweekday(df):
     byweekday_df = df.groupby('weekday').agg({
          'cnt': 'mean',
          'registered': 'mean',
          'casual': 'mean'
     }).reset_index()

     byweekday_df.rename(columns={
     'cnt': 'avg_total_user',
     'registered': 'avg_registered_user',
     'casual': 'avg_casual_user'
     }, inplace=True)
     
     #ubah format nama hari
     weekday_mapping = {
     0: 'minggu', 1: 'senin', 2: 'selasa', 3: 'rabu', 
     4: 'kamis', 5: 'jumat', 6: 'sabtu'
     }
     byweekday_df['weekday'] = byweekday_df['weekday'].map(weekday_mapping)

     return byweekday_df

def create_bymonth(df):
     bymonth_df = df.resample(rule= 'M', on='dteday' ).agg({
          'cnt': 'mean',
          'registered': 'mean',
          'casual': 'mean'
     }).reset_index()

     #ubah format tanggal ke bulan
     bymonth_df['dteday'] = bymonth_df['dteday'].dt.strftime('%B')

     #ubah nama kolom
     bymonth_df.columns = ['month', 'avg_total_user', 'avg_registered_user', 'avg_casual_user']

     return bymonth_df

def create_byseason(df):
     byseason_df = df.groupby('season').agg({
          'cnt': 'mean',
          'registered': 'mean',
          'casual': 'mean'
     }).reset_index()

     byseason_df.columns = ['season','avg_total_user', 'avg_registered_user', 'avg_casual_user']

     #ubah format nama season
     byseason_df['season'] = byseason_df.season.apply(lambda s: 'springer' if s==1 else('summer'if  s==2 else ('fall' if s==3 else 'winter')))

     return byseason_df

def create_byweathersit(df):
     byweathersit_df = df.groupby('weathersit').agg({
          'cnt': 'mean',
          'registered': 'mean',
          'casual': 'mean'
     }).reset_index()

     #ubah nama column
     byweathersit_df.columns = ['weathersit','avg_total_user', 'avg_registered_user', 'avg_casual_user']

     return byweathersit_df

def create_byday(df):
     byday_df = df.resample(rule='d', on='dteday').agg({
          'cnt': 'sum',
          'registered': 'sum',
          'casual': 'sum',
          'temp': 'mean'
     }).reset_index()

     byday_df.columns = ['tanggal','sum_total_user', 'sum_registered_user', 'sum_casual_user', 'avg_suhu']

     
     return byday_df

data = pd.read_csv('hour.csv')

#merubah tipe data dteday ke datetime
data['dteday'] = pd.to_datetime(data['dteday'])

#merubah format tahun
data['yr'] = data.dteday.apply(lambda x: x.strftime('%Y'))

#merubah format jam (1-24)
data['hr'] = data.hr.apply(lambda x: x+1)

#merubah tipe data workingday menjadi boolean
data['workingday'] = data.workingday.apply(lambda x: True if x == 1 else False)

#ubah format temperatur ke Celcius
data['temp'] = data.temp.apply(lambda t: round(t*41,2))

min_date = data['dteday'].min()
max_date = data['dteday'].max()

with st.sidebar:
     st.title('Dashboard Rental Sepeda 🚲')

     start_date, end_date = st.date_input(
          label= 'Rentang waktu',
          min_value = min_date,
          max_value= max_date,
          value=[min_date, max_date]
     )

     tipe_user = st.selectbox(
          label='Tipe Pengguna',
          options=('all', 'registered', 'casual')
     )

main_df = data[(data['dteday'] >= str(start_date)) & (data['dteday'] <= str(end_date))]

byday_df = create_byday(main_df)
byhour_df = create_byhour(main_df)
byweekday_df = create_byweekday(main_df)
byweathersit_df = create_byweathersit(main_df)
bymonth_df = create_bymonth(main_df)
byseason_df = create_byseason(main_df)

st.header('Dashboard Rental Sepeda')
st.subheader('Performa Pengguna Rental Sepeda 🚲')

user_sum = byday_df.sum_total_user.sum()
registered_user_sum = byday_df.sum_registered_user.sum()
casual_user_sum = byday_df.sum_casual_user.sum()

#grafik perform
fig1, ax1= plt.subplots(figsize=(16,8))

fig2, ax2 = plt.subplots(
    nrows=1, ncols=2,  
    figsize=(12, 5), 
    gridspec_kw={"width_ratios": [1, 3]}  
)
#pie chart
ax2[0].pie(
     x=(byday_df['sum_casual_user'].mean(), byday_df['sum_registered_user'].mean()),
     labels=('Casual', 'Registered'),
     autopct='%1.1f%%',
     colors=['#DD8452','#55A868'],
)
ax2[0].set_title("Distribusi Tipe Pengguna", fontsize=20)

#barchart byweathersit
labels = ['Clear, Few clouds, Partly cloudy, Partly cloudy','Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist', 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds', 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog']
biru = mpatches.Patch(color='#4C72B0')
orange = mpatches.Patch(color='#DD8452')
hijau = mpatches.Patch(color='#55A868')
merah = mpatches.Patch(color='#C44E52')

ax2[1].legend(handles=[biru, orange, hijau, merah],labels=labels, loc='upper left', bbox_to_anchor=(0, 0), fontsize=12)
ax2[1].set_title("Rata-Rata Pengguna Berdasrkan Cuaca", fontsize=20)
ax2[1].yaxis.set_label_position('right')
ax2[1].yaxis.tick_right()
ax2[1].set_ylabel('Rata-rata pengguna')
fig2.tight_layout()

#korelasi suhu dan pengguna
fig3, ax3 = plt.subplots(figsize=(11,6))
ax3.set_xlabel('Rata-Rata Suhu (C)')
ax3.set_ylabel('Total Pengguna')

#perbedaan pengguna per jam, hari
fig4, ax4 = plt.subplots(1, 2, figsize=(16,8))
ax4[0].set_ylabel('Rata-Rata Pengguna/Jam', fontsize=14)
ax4[0].set_xlabel('Jam',fontsize=14)
ax4[0].set_title('Rata-Rata Perbedaan Pengguna Per Jam')
ax4[1].set_ylabel('Rata-Rata Pengguna/Hari', fontsize=14)
ax4[1].set_ylabel('Hari',fontsize=14)
ax4[1].set_title('Rata-Rata Perbedaan Pengguna Per Hari')

#perbedaan pengguna per month dan season
fig5, ax5 = plt.subplots(1, 2, figsize=(16,8), gridspec_kw={"width_ratios": [3, 1]} )
ax5[0].set_title('Rata-Rata Perbedaan Pengguna Per Bulan')
ax5[0].tick_params(axis='x', labelsize=9)
ax5[0].set_ylabel('Rata-Rata Pengguna/Bulan', fontsize=14)
ax5[0].set_xlabel('Bulan', fontsize=14)
ax5[1].set_title('Rata-Rata Perbedaan Pengguna Per Musim')
ax5[1].set_ylabel('Rata-Rata Pengguna/Musim', fontsize=14)
ax5[1].set_xlabel('Musim', fontsize=14)

if tipe_user == 'all':
     st.metric('Total Pengguna:', value=user_sum)

     #grafik performa
     ax1.plot(byday_df["tanggal"], byday_df["sum_total_user"], linewidth=3, color='#C44E52', label='Total User') 
     ax1.plot(byday_df["tanggal"], byday_df["sum_casual_user"], marker='', linewidth=3, color='#DD8452', label='Casual User') 
     ax1.plot(byday_df["tanggal"], byday_df["sum_registered_user"], marker='', linewidth=3, color='#55A868', label='Registered User') 
     ax1.legend(fontsize=14)

     st.pyplot(fig1)

     st.subheader('Korelasi Suhu Udara dan Bayak Pengguna')
     #korelasi suhu udara dan banyak pengguna
     sns.scatterplot(y=byday_df['sum_total_user'],x=byday_df['avg_suhu'], color='black', ax=ax3)
     sns.regplot(y=byday_df['sum_total_user'],x=byday_df['avg_suhu'], color='blue', ax=ax3)
     st.pyplot(fig3)
     
     sns.barplot(x=byweathersit_df['weathersit'], y=byweathersit_df['avg_total_user'], data=byweathersit_df, ax=ax2[1], palette='tab10')
     st.pyplot(fig2)
     
     st.subheader('Perbedaan Pengguna Per Jam, Hari, Bulan, dan Musim')
     #grafik perbedaan pengguna berdasarkan jam
     colors_for_hour = [ '#C44E52' if i == byhour_df['avg_total_user'].idxmax() else  '#4C72B0' for i in range(len(byhour_df))]
     sns.barplot(y=byhour_df['avg_total_user'], x=byhour_df['hour'], data=byhour_df, palette=colors_for_hour, ax=ax4[0])
     #grafik perbedaan pengguna berdasarkan hari
     colors_for_weekday = [ '#C44E52' if i == byweekday_df['avg_total_user'].idxmax() else  '#4C72B0' for i in range(len(byweekday_df))]
     sns.barplot(y=byweekday_df['avg_total_user'], x=byweekday_df['weekday'], data=byweekday_df, palette=colors_for_weekday, ax=ax4[1])
     st.pyplot(fig4)

     #grafik perbedaan pengguna berdasarkan month
     colors_for_month = [ '#C44E52' if i == bymonth_df['avg_total_user'].idxmax() else  '#4C72B0' for i in range(len(bymonth_df))]
     sns.barplot(y=bymonth_df['avg_total_user'], x=bymonth_df['month'], data=bymonth_df, palette=colors_for_month, ax=ax5[0])
     #grafik perbedaan pengguna berdasarkan season
     colors_for_season = [ '#C44E52' if i == byseason_df['avg_total_user'].idxmax() else  '#4C72B0' for i in range(len(byseason_df))]
     sns.barplot(y=byseason_df['avg_total_user'], x=byseason_df['season'], data=byseason_df, palette=colors_for_season, ax=ax5[1])
     st.pyplot(fig5)

elif tipe_user == 'registered':
     st.metric('Total Pengguna:', value=casual_user_sum)

     ax1.plot(byday_df["tanggal"], byday_df["sum_registered_user"], marker='', linewidth=3, color='#55A868', label='Registered User') 
     ax1.legend(fontsize=14)

     st.pyplot(fig1)
     
     st.subheader('Korelasi Suhu Udara dan Bayak Pengguna')
     #korelasi suhu udara dan banyak pengguna
     sns.scatterplot(y=byday_df['sum_registered_user'],x=byday_df['avg_suhu'],color='black', ax=ax3)
     sns.regplot(y=byday_df['sum_registered_user'],x=byday_df['avg_suhu'], color='blue', ax=ax3)
     st.pyplot(fig3)
    
     sns.barplot(x=byweathersit_df['weathersit'], y=byweathersit_df['avg_registered_user'], data=byweathersit_df, ax=ax2[1], palette='tab10')
     st.pyplot(fig2)

     st.subheader('Perbedaan Pengguna Per Jam, Hari, Bulan, dan Musim')
     #grafik perbedaan pengguna berdasarkan jam
     colors_for_hour = [ '#C44E52' if i == byhour_df['avg_registered_user'].idxmax() else  '#4C72B0' for i in range(len(byhour_df))]
     sns.barplot(y=byhour_df['avg_registered_user'], x=byhour_df['hour'], data=byhour_df, palette=colors_for_hour, ax=ax4[0])
     #grafik perbedaan pengguna berdasarkan hari
     colors_for_weekday = [ '#C44E52' if i == byweekday_df['avg_registered_user'].idxmax() else  '#4C72B0' for i in range(len(byweekday_df))]
     sns.barplot(y=byweekday_df['avg_registered_user'], x=byweekday_df['weekday'], data=byweekday_df, palette=colors_for_weekday, ax=ax4[1])
     st.pyplot(fig4)

     #grafik perbedaan pengguna berdasarkan month
     colors_for_month = [ '#C44E52' if i == bymonth_df['avg_registered_user'].idxmax() else  '#4C72B0' for i in range(len(bymonth_df))]
     sns.barplot(y=bymonth_df['avg_registered_user'], x=bymonth_df['month'], data=bymonth_df, palette=colors_for_month, ax=ax5[0])
     #grafik perbedaan pengguna berdasarkan season
     colors_for_season = [ '#C44E52' if i == byseason_df['avg_registered_user'].idxmax() else  '#4C72B0' for i in range(len(byseason_df))]
     sns.barplot(y=byseason_df['avg_registered_user'], x=byseason_df['season'], data=byseason_df, palette=colors_for_season, ax=ax5[1])
     st.pyplot(fig5)

elif tipe_user == 'casual':
     st.metric('Total Pengguna:', value=registered_user_sum)
     ax1.plot(byday_df["tanggal"], byday_df["sum_casual_user"], marker='', linewidth=3, color='#DD8452', label='Casual User') 
     ax1.legend(fontsize=14)
     
     st.pyplot(fig1)
     
     st.subheader('Korelasi Suhu Udara dan Bayak Pengguna')
     #korelasi suhu udara dan banyak pengguna
     sns.scatterplot(y=byday_df['sum_casual_user'],x=byday_df['avg_suhu'], color='black', ax=ax3)
     sns.regplot(y=byday_df['sum_casual_user'],x=byday_df['avg_suhu'], color='blue', ax=ax3)
     st.pyplot(fig3)
   
     sns.barplot(x=byweathersit_df['weathersit'], y=byweathersit_df['avg_casual_user'], data=byweathersit_df, ax=ax2[1], palette='tab10')
     st.pyplot(fig2)

     st.subheader('Perbedaan Pengguna Per Jam, Hari, Bulan, dan Musim')
     #grafik perbedaan pengguna berdasarkan jam
     colors_for_hour = [ '#C44E52' if i == byhour_df['avg_casual_user'].idxmax() else  '#4C72B0' for i in range(len(byhour_df))]
     sns.barplot(y=byhour_df['avg_casual_user'], x=byhour_df['hour'], data=byhour_df, palette=colors_for_hour, ax=ax4[0])
     #grafik perbedaan pengguna berdasarkan hari
     colors_for_weekday = [ '#C44E52' if i == byweekday_df['avg_casual_user'].idxmax() else  '#4C72B0' for i in range(len(byweekday_df))]
     sns.barplot(y=byweekday_df['avg_casual_user'], x=byweekday_df['weekday'], data=byweekday_df, palette=colors_for_weekday, ax=ax4[1])
     st.pyplot(fig4)

     #grafik perbedaan pengguna berdasarkan month
     colors_for_month = [ '#C44E52' if i == bymonth_df['avg_casual_user'].idxmax() else  '#4C72B0' for i in range(len(bymonth_df))]
     sns.barplot(y=bymonth_df['avg_casual_user'], x=bymonth_df['month'], data=bymonth_df, palette=colors_for_month, ax=ax5[0])
     #grafik perbedaan pengguna berdasarkan season
     colors_for_season = [ '#C44E52' if i == byseason_df['avg_casual_user'].idxmax() else  '#4C72B0' for i in range(len(byseason_df))]
     sns.barplot(y=byseason_df['avg_casual_user'], x=byseason_df['season'], data=byseason_df, palette=colors_for_season, ax=ax5[1])
     st.pyplot(fig5)