import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("tasks_2025-07-17_14_28_56.csv")
df.columns = ["Tarefa", "Andamento", "Responsavel"] + df.columns.tolist()[3:]
df["Andamento"] = pd.to_numeric(df["Andamento"], errors="coerce")

st.set_page_config(layout="wide")
st.title("Dashboard de Andamento de Projetos")

responsaveis = df["Responsavel"].dropna().unique().tolist()
responsavel_sel = st.sidebar.multiselect("Filtrar por responsável:", responsaveis, default=responsaveis)
df_filtrado = df[df["Responsavel"].isin(responsavel_sel)]

col1, col2 = st.columns(2)
col1.metric("Andamento Médio", f"{df_filtrado['Andamento'].mean():.1f}%")
col2.metric("Total de Tarefas", f"{df_filtrado.shape[0]}")

df_resp = df_filtrado.groupby("Responsavel")["Andamento"].mean().reset_index()
fig_resp = px.bar(df_resp, x="Responsavel", y="Andamento", title="Média de Andamento por Responsável", color="Responsavel", text_auto=True)
st.plotly_chart(fig_resp, use_container_width=True)

faixas = pd.cut(df_filtrado["Andamento"], bins=[-1, 0, 50, 80, 100], labels=["0%", "1-50%", "51-80%", "81-100%"])

if not faixas.empty and faixas.notna().any():
    fig_pizza = px.pie(
        faixas.value_counts().reset_index(),
        names="index",
        values="count",
        title="Distribuição por Faixa de Andamento"
    )
    st.plotly_chart(fig_pizza, use_container_width=True)
else:
    st.warning("Nenhum dado disponível para gerar o gráfico de pizza.")


st.subheader("Tarefas em Andamento")
st.dataframe(df_filtrado.sort_values("Andamento", ascending=False), use_container_width=True)
