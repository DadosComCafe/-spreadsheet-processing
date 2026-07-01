import duckdb
from pydantic import BaseModel, model_validator, ValidationError
from typing import Any, Dict, List


def validar_nome(dados: Dict[str, Any]):
    nome = dados.get("nome")
    if not nome or str(nome).strip() == "":
        raise ValueError("Nome não pode ser vazio")

def validar_idade(dados: Dict[str, Any]):
    idade = dados.get("idade")
    if idade is not None and int(idade) <= 0:
        raise ValueError("Idade deve ser maior que zero")


LISTA_DE_VALIDADORES = [validar_nome, validar_idade]



class LinhaPlanilha(BaseModel):
    model_config = {"extra": "allow"} 
    linha_id: int


    @model_validator(mode="after")
    def executar_validadores_customizados(self) -> "LinhaPlanilha":
        dados_linha = self.model_dump()
        

        for validador in LISTA_DE_VALIDADORES:
            validador(dados_linha)
            
        return self



def executar_validacao_sistema(caminho_excel: str) -> Dict[int, List[str]]:
    con = duckdb.connect(database=":memory:")
    con.execute("INSTALL spatial; LOAD spatial;")


    query = "SELECT ROW_NUMBER() OVER () AS linha_id, * FROM st_read(?)"
    df_arrow = con.execute(query, [caminho_excel]).arrow()
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