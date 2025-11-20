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
st.markdown("Este aplicativo lê os dados da planilha e exibe-os em formato de tabela (Descrição e Valor).")

# --- Carregamento e Tratamento dos Dados ---
try:
    # Verifica se o arquivo existe
    if not os.path.exists(FILE_PATH):
        st.error(
            f"Erro: O arquivo '{FILE_PATH}' não foi encontrado no diretório. Certifique-se de que o arquivo Excel (.xlsx) esteja na mesma pasta.")
        st.stop()

    # Tenta carregar o arquivo Excel
    try:
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    except Exception as e:
        st.error(
            f"Erro ao ler o arquivo Excel. Verifique se a biblioteca 'openpyxl' está instalada e o nome da planilha ('{SHEET_NAME}') está correto. Detalhes: {e}")
        st.stop()

    # Processamento dos dados
    required_columns = ['Descrição', 'Valor']

    # Verifica se as colunas necessárias existem
    if not all(col in df.columns for col in required_columns):
        st.error("Erro: As colunas 'Descrição' e/ou 'Valor' não foram encontradas na planilha.")
        st.write("Colunas encontradas:", df.columns.tolist())
    else:
        # Converte a coluna 'Valor' para tipo numérico
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

        # Remove linhas onde 'Valor' é inválido
        df.dropna(subset=['Valor'], inplace=True)

        # Ordena os dados (opcional)
        df = df.sort_values(by='Valor', ascending=False)

        # --- Exibição da Tabela ---
        # O gráfico foi removido. Exibindo a tabela conforme solicitado.
        st.header("📋 Tabela de Descrição e Valor")

        # Seleciona apenas as colunas 'Descrição' e 'Valor' para exibição
        df_display = df[['Descrição', 'Valor']]

        # Exibe a tabela com as colunas necessárias e usa a largura total do container
        st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")