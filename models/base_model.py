from pydantic import BaseModel, model_validator, ValidationError
from typing import Any, Dict, List
from validators.content_validator import LISTA_DE_VALIDADORES

class LinhaPlanilha(BaseModel):
    model_config = {"extra": "allow"} 
    linha_id: int


    @model_validator(mode="after")
    def executar_validadores_customizados(self) -> "LinhaPlanilha":
        dados_linha = self.model_dump()
        

        for validador in LISTA_DE_VALIDADORES:
            validador(dados_linha)
            
        return self