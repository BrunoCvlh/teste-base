import streamlit as st
import pandas as pd
import os

# --- Configuração da Página ---
st.set_page_config(
    page_title="Visualizador de Valores",
    layout="wide"
)

# --- Caminho do Arquivo ---
# Renomeie seu arquivo original para 'Book1.xlsx' ou ajuste o nome abaixo.
# ASSUMINDO que o arquivo .xlsx está na mesma pasta.
FILE_PATH = "Book1.xlsx"
SHEET_NAME = "Sheet1"  # Se sua planilha tiver outro nome, ajuste aqui.

st.title("💰 Visualização de Valores por Item")
st.markdown("Este aplicativo lê os dados da planilha e exibe um gráfico de barras.")

# --- Carregamento e Tratamento dos Dados ---
try:
    if not os.path.exists(FILE_PATH):
        st.error(
            f"Erro: O arquivo '{FILE_PATH}' não foi encontrado no diretório. Certifique-se de que o arquivo Excel (.xlsx) esteja na mesma pasta.")
        st.stop()

    # CORREÇÃO PRINCIPAL: Usando pd.read_excel para carregar o arquivo .xlsx
    try:
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel. Verifique se a biblioteca 'openpyxl' está instalada. Detalhes: {e}")
        st.stop()

    # Processamento dos dados
    required_columns = ['Descrição', 'Valor']

    # Verifica se as colunas necessárias existem
    if not all(col in df.columns for col in required_columns):
        st.error("Erro: As colunas 'Descrição' e/ou 'Valor' não foram encontradas na planilha.")
        st.write("Colunas encontradas:", df.columns.tolist())
    else:
        # Converte a coluna 'Valor' para tipo numérico
        # O Excel lida melhor com formatos numéricos, mas este passo é uma segurança
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        # Remove linhas onde 'Valor' é inválido
        df.dropna(subset=['Valor'], inplace=True)

        # Ordena os dados (opcional)
        df = df.sort_values(by='Valor', ascending=False)

        # --- Exibição do Gráfico ---
        st.header("📊 Gráfico de Valores por Item")

        st.bar_chart(
            data=df,
            x='Descrição',
            y='Valor',
            height=500
        )

        # --- Exibição da Tabela (Opcional) ---
        st.header("📋 Dados Processados")
        st.dataframe(df)

except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")