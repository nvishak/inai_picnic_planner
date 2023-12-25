from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Location
from app.schemas import LocationCreate, LocationUpdate


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    def get_all(
        self, db: Session
    ) -> List[Location]:
        return (
            db.query(self.model)
            .all()
        )


location = CRUDLocation(Location)
