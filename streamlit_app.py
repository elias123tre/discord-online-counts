# %%
import streamlit as st
import pandas as pd

# %%

st.write("""
# Online Status
This app shows the online status of the KTH Computer Science students.
Data is collected from the [KTH Computer Science Discord server](https://discord.gg/datasektionen) and Discord server of the [KTH Computer Science students](https://discord.gg/8zStbfHdaF).
""")

SERVERS = {
    "Konglig Datasektionen": "https://onlinestatus.elias1233.se/Konglig_Datasektionen_datasektionen.csv",
    "Datateknik 2021": "https://onlinestatus.elias1233.se/Datateknik_2021_8zStbfHdaF.csv"
}

server = st.selectbox("Select server", SERVERS.keys())

# %%
storage_options = {"User-Agent": "Mozilla/5.0"}

url = SERVERS[server]

df = pd.read_csv(url, storage_options=storage_options)
# convert Datetime to datetime
df["Datetime"] = pd.to_datetime(df["Datetime"])
# set Datetime as index
df.set_index("Datetime", inplace=True)

# print(df.head())

# plot the dataframe as a bar chart
# df.plot(y="Active Users")

st.bar_chart(df, y="Active Users")