from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.TransformerModel import (
    TransformerModel,
)
from api.electrical.repositories.TransformerRepo import (
    TransformerRepo,
)
from api.electrical.schemas.TransformerSchema import (
    TransformerBase,
    CreateTransformer,
)


#
class TransformerService:
    transformer: TransformerRepo

    def __init__(
        self, transformer: TransformerRepo = Depends()
    ) -> None:
        self.transformer = transformer

    # get all transformers function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[TransformerModel]:
        return self.transformer.list(skip=skip, limit=limit)

    # get transformer by id function
    async def get(self, id: int) -> TransformerModel:
        return self.transformer.get(id=id)

    # get transformer by number function
    async def getbynumber(
        self, number: str
    ) -> TransformerBase:
        return self.transformer.getbynumber(number=number)

    # get transformer by name function
    async def getbyname(self, name: str) -> TransformerBase:
        return self.transformer.getbyname(name=name)

    # create transformer function
    async def create(
        self, data: List[CreateTransformer]
    ) -> List[CreateTransformer]:
        for item in data:
            transformer = self.transformer.getbycode(
                code=item.code
            )
            if transformer:
                raise HTTPException( 
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transformer already registered with code "
                    + str(item.code),
                )

            transformer = self.transformer.getbytransformernumber(
                number=item.transformer_number
            )
            if transformer:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transformer already registered with transformer_number "
                    + str(item.transformer_number),
                )

            # transformer = self.transformer.getbyname(
            #     name=item.infos.name
            # )
            # if transformer:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Transformer already registered with name "
            #         + item.infos.name,
            #     )

        return self.transformer.create(data=data)

    # update transformer function
    async def update(
        self, number: int, data: TransformerBase
    ) -> TransformerModel:
        transformer = self.transformer.getbynumber(
            number=number
        )
        if transformer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transformer not found",
            )

        transformerdict = data.dict(exclude_unset=True)
        for key, val in transformerdict.items():
            setattr(transformer, key, val)
        return self.transformer.update(transformer)

    # delete transformer function
    async def delete(
        self, transformer: TransformerModel
    ) -> None:
        transformer = self.transformer.get(id=id)
        if transformer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transformer not found",
            )

        self.transformer.update(transformer)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Transformer deleted",
        )
