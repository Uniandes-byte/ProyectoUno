from pydantic import BaseModel

class DataModel(BaseModel):
    # Estas varibles permiten que la librería pydantic haga el parseo entre el

    review_es: str

    def columns(self):
        return ["review_es"]