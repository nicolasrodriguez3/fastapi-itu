from typing import List
from app.database import database_connection
from app.database.models import ClaimModel


class ClaimsRepository:
    def __init__(self):
        self.db = database_connection.session

    def create(self, new_claim_dict: dict) -> dict:
        new_claim = ClaimModel(**new_claim_dict)
        self.db.add(new_claim)
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        self.db.refresh(new_claim)
        return new_claim.to_dict()

    def get_list(self, limit: int, offset: int, user_id: int) -> List[dict]:
        claims = (
            self.db.query(ClaimModel)
            .filter_by(user_id=user_id)
            .order_by("id")
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [claim.to_dict() for claim in claims]

    def get_by_id(self, claim_id: int) -> dict | None:
        claim = self.__get_one(claim_id)
        if claim is None:
            return None
        return claim.to_dict()

    def update(self, claim_id: int, new_data: dict) -> dict | None:
        claim = self.__get_one(claim_id)
        if claim is None:
            return None
        for key, value in new_data.items():
            setattr(claim, key, value)

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        self.db.refresh(claim)
        return claim.to_dict()

    def delete(self, claim_id: int) -> bool:
        claim = self.__get_one(claim_id)
        if claim is None:
            return False

        try:
            self.db.delete(claim)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        return True

    def __get_one(self, claim_id: int) -> ClaimModel | None:
        return self.db.query(ClaimModel).filter(ClaimModel.id == claim_id).first()
