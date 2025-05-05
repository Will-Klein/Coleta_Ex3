import pandas as pd

csv_file = 'agents_pick_rates.csv'

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
        df = pd.read_csv(csv_file)

        if not df.empty and "id" in df.columns:
            next_id = df["id"].max() + 1
        else:
            next_id = 1

        data["id"] = next_id

        new_data = pd.DataFrame([data])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(csv_file, index=False)
        return "Dados inseridos com sucesso!"

    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados: {e}")
        return "Erro ao inserir os dados."

def deletar_championship(data):
    try:
        if "id" not in data:
            return {
                "mensagem": "Campo 'id' ausente.",
                "status_code": 400
            }

        df = pd.read_csv(csv_file)

        id_value = data["id"]
        if id_value not in df["id"].values:
            return {"mensagem": "Campeonato com o ID fornecido não encontrado.", "status_code": 404}

        df = df[df["id"] != id_value]

        df.to_csv(csv_file, index=False)
        return {"mensagem": "Linha deletada com sucesso!", "status_code": 200}

    except Exception as e:
        print(f"Ocorreu um erro ao deletar os dados: {e}")
        return {"mensagem": "Erro interno no servidor.", "status_code": 500}
    
def atualizar_championship(data):
    try:
        if "id" not in data:
            return {
                "mensagem": "Campo 'id' ausente.",
                "status_code": 400
            }

        df = pd.read_csv(csv_file)

        id_value = data["id"]
        if id_value not in df["id"].values:
            return {"mensagem": "Campeonato com o ID fornecido não encontrado.", "status_code": 404}

        for field, value in data.items():
            if field != "id" and field in df.columns:
                df.loc[df["id"] == id_value, field] = value

        df.to_csv(csv_file, index=False)
        return {"mensagem": "Linha atualizada com sucesso!", "status_code": 200}
        
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar os dados: {e}")
        return {"mensagem": "Erro interno no servidor.", "status_code": 500}