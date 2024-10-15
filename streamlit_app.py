# %%
import streamlit as st
import pandas as pd

# %%

st.set_page_config(page_title="Discord Online Counts", page_icon=":bar_chart:")

st.title("Online members of KTH Computer Science Discord servers")

st.write("""
This app shows the online member count of the KTH Computer Science Discord servers.
Data is collected from the [Konglig Datasektionen](https://discord.gg/datasektionen) and [Datateknik 2021](https://discord.gg/8zStbfHdaF) Discord servers.
""")

SERVERS = {
    "Konglig Datasektionen": "https://onlinestatus.elias1233.se/Konglig_Datasektionen_mGwN8HbJaK.csv",
    "Datateknik 2021": "https://onlinestatus.elias1233.se/Datateknik_2021_8zStbfHdaF.csv",
}

server = st.selectbox("Select server", SERVERS.keys())

# %%
storage_options = {"User-Agent": "Mozilla/5.0"}

url = SERVERS[server]

df = pd.read_csv(url, storage_options=storage_options)
df["Datetime"] = pd.to_datetime(df["Datetime"])
df.set_index("Datetime", inplace=True)

st.bar_chart(df, y="Active Users")
