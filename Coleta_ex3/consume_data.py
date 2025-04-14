import pandas as pd

# Caminho para o arquivo CSV
csv_file = 'agents_pick_rates.csv'

# Lendo o arquivo CSV
def consulta_csv():
    try:
        data = pd.read_csv(csv_file)
        print("Dados carregados com sucesso!")
        return data
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_file}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o arquivo: {e}")