import duckdb
from pydantic import ValidationError
from typing import Dict, List
from models.base_model import LinhaPlanilha

def executar_validacao_sistema(caminho_excel: str) -> Dict[int, List[str]]:
    con = duckdb.connect(database=":memory:")
    con.execute("INSTALL spatial; LOAD spatial;")
    
    query = "SELECT ROW_NUMBER() OVER () AS linha_id, * FROM st_read(?)"
    
    arrow_reader = con.execute(query, [caminho_excel]).arrow()
    df_arrow = arrow_reader.read_all()
    
    dados_planilha = df_arrow.to_pydict()
    erros_finais = {}
    
    qtd_linhas = len(dados_planilha["linha_id"])
    chaves = dados_planilha.keys()
    
    for i in range(qtd_linhas):
        dados_linha = {k: dados_planilha[k][i] for k in chaves}
        linha_id = dados_linha["linha_id"]
        try:
            LinhaPlanilha(**dados_linha)
        except ValidationError as e:
            mensagens = [erro["msg"].split(", ")[-1] for erro in e.errors()]
            erros_finais[linha_id] = mensagens
    return erros_finais


if __name__ == "__main__":
    file = "teste.xlsx"
    try:
        erros = executar_validacao_sistema(caminho_excel=file)
        print("Processamento concluído com sucesso!")
        if erros:
            print(f"Linhas com erros encontradas: {len(erros)}")
        else:
            print("Nenhum erro encontrado na planilha.")
    except Exception as e:
        print(f"False: {e}")