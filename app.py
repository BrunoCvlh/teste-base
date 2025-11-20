import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Visualizador de Valores",
    layout="wide"
)

FILE_PATH = "Book1.csv"

st.title("💰 Visualização de Valores por Item")
st.markdown("Este aplicativo lê os dados do arquivo CSV e exibe-os em formato de tabela (Descrição e Valor).")

try:
    if not os.path.exists(FILE_PATH):
        st.error(
            f"Erro: O arquivo '{FILE_PATH}' não foi encontrado no diretório. Certifique-se de que o arquivo CSV (.csv) esteja na mesma pasta.")
        st.stop()

    try:
        df = pd.read_csv(FILE_PATH)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV. Verifique se o formato e o delimitador estão corretos. Detalhes: {e}")
        st.stop()

    required_columns = ['Descrição', 'Valor']

    if not all(col in df.columns for col in required_columns):
        st.error("Erro: As colunas 'Descrição' e/ou 'Valor' não foram encontradas no arquivo CSV.")
        st.write("Colunas encontradas:", df.columns.tolist())
    else:
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        df.dropna(subset=['Valor'], inplace=True)

        df = df.sort_values(by='Valor', ascending=False)

        st.header("📋 Tabela de Descrição e Valor")

        df_display = df[['Descrição', 'Valor']]

        st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")