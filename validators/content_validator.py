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