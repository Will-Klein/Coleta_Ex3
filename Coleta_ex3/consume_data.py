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

def inserir_championship(data):
    try:
        # Lê o arquivo CSV existente
        df = pd.read_csv(csv_file)

        # Adiciona os novos dados
        new_data = pd.DataFrame([data])
        df = pd.concat([df, new_data], ignore_index=True)

        # Salva o DataFrame atualizado de volta no CSV
        df.to_csv(csv_file, index=False)
        return "Dados inseridos com sucesso!"
    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados: {e}")

def deletar_championship(data):
    try:
        # Verifica se todos os campos necessários estão presentes no JSON
        required_fields = ["Tournament", "Stage", "Match Type", "Map", "Agent", "Pick Rate"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {
                "mensagem": f"Campos ausentes: {', '.join(missing_fields)}",
                "status_code": 400
            }

        # Lê o arquivo CSV existente
        df = pd.read_csv(csv_file)

        # Constrói a condição para identificar a linha a ser removida
        condition = True
        for coluna, valor in data.items():
            condition &= (df[coluna] == valor)

        # Verifica se alguma linha atende à condição
        if not condition.any():
            return {"mensagem": "Campeonato não encontrado.", "status_code": 404}

        # Remove a linha que atende à condição
        df = df[~condition]

        # Salva o DataFrame atualizado de volta no CSV
        df.to_csv(csv_file, index=False)
        return {"mensagem": "Linha deletada com sucesso!", "status_code": 200}
    except Exception as e:
        print(f"Ocorreu um erro ao deletar os dados: {e}")
        return {"mensagem": "Erro interno no servidor.", "status_code": 500}
    
def atualizar_championship(data):
    try:
        # Verifica se todos os campos necessários estão presentes no JSON
        required_fields = ["Tournament", "Stage", "Match Type", "Map", "Agent", "Pick Rate"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {
                "mensagem": f"Campos ausentes: {', '.join(missing_fields)}",
                "status_code": 400
            }

        # Lê o arquivo CSV existente
        df = pd.read_csv(csv_file)

        # Constrói a condição para identificar a linha a ser atualizada
        condition = True
        for coluna, valor in data.items():
            if coluna != "Pick Rate":  # Ignora o campo que será atualizado
                condition &= (df[coluna] == valor)

        # Verifica se alguma linha atende à condição
        if not condition.any():
            return {"mensagem": "Campeonato não encontrado.", "status_code": 404}

        # Atualiza o campo 'Pick Rate' na linha correspondente
        df.loc[condition, "Pick Rate"] = data["Pick Rate"]

        # Salva o DataFrame atualizado de volta no CSV
        df.to_csv(csv_file, index=False)
        return {"mensagem": "Campeonato atualizado com sucesso!", "status_code": 200}
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar os dados: {e}")
        return {"mensagem": "Erro interno ao atualizar o campeonato.", "status_code": 500}