import pandas as pd
import streamlit as st
import plotly.express as px
import time

st.set_page_config(page_title="Streaming Processing Dashboard", layout="wide")

st.title("⚡ Streaming Processing Dashboard")
st.write("Sipariş verileri tek tek işleniyor ve dashboard canlı olarak güncelleniyor.")

df = pd.read_csv("orders.csv")

placeholder = st.empty()

total_orders = 0
delayed_orders = 0
cancelled_orders = 0
live_data = []

for index, row in df.iterrows():
    total_orders += 1

    if row["status"] == "delayed":
        delayed_orders += 1

    if row["status"] == "cancelled":
        cancelled_orders += 1

    live_data.append(row)
    live_df = pd.DataFrame(live_data)

    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Toplam Sipariş", total_orders)
        col2.metric("Ortalama Teslimat Süresi", f"{live_df['delivery_time'].mean():.2f} dk")
        col3.metric("Geciken Sipariş", delayed_orders)
        col4.metric("İptal Edilen Sipariş", cancelled_orders)

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            fig1 = px.pie(live_df, names="status", title="Sipariş Durumu")
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            restoran = live_df["restaurant_type"].value_counts().reset_index()
            restoran.columns = ["restaurant_type", "count"]

            fig2 = px.bar(
                restoran,
                x="restaurant_type",
                y="count",
                title="Restoran Türüne Göre Sipariş"
            )
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:
            fig3 = px.histogram(
                live_df,
                x="delivery_time",
                title="Teslimat Süresi Dağılımı"
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            fig4 = px.line(
                x=live_df.index,
                y=live_df["delivery_time"],
                markers=True,
                title="Canlı Teslimat Süresi Akışı"
            )
            st.plotly_chart(fig4, use_container_width=True)

        st.subheader("📋 Canlı Sipariş Akışı")
        st.dataframe(live_df, use_container_width=True)

    time.sleep(2)