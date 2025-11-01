from pydantic import BaseModel

class ContractRequest(BaseModel):
    code: str
