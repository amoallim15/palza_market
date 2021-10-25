from fastapi import Depends, HTTPException
from src.core.model import SuccessModel, ListModel
from src.models.user import UserModel
from src.models.realstate import RealstateModel
from src.core.enums import UserType
from src.core.utils import get_agency_info


def main(app):
    #
    @app.get("/health", response_model=SuccessModel)
    async def info():
        return SuccessModel(detail="OK.")

    @app.get("/lookup/agency", response_model=ListModel)
    async def agencies(text: str = "", current_user=Depends(app.current_user)):
        cursor = (
            await app.db["users"]
            .find({"user_type": UserType.AGENCY, "display_name": {"$regex": text}})
            .limit(10)
        )
        data_list = []
        #
        async for user in cursor:
            data_list.append(UserModel(**user))
        #
        count = len(data_list)
        result = {
            "data": data_list,
            "info": {"page": 0, "count": count, "page_size": count},
        }
        #
        return ListModel(**result)

    @app.get("/lookup/realstate", response_model=ListModel)
    async def realstates(text: str = "", current_user=Depends(app.current_user)):
        cursor = (
            await app.db["realstates"]
            .find({"display_name": {"$regex": text}})
            .limit(10)
        )
        data_list = []
        #
        async for realstate in cursor:
            data_list.append(RealstateModel(**realstate))
        #
        count = len(data_list)
        result = {
            "data": data_list,
            "info": {"page": 0, "count": count, "page_size": count},
        }
        #
        return ListModel(**result)

    @app.get("/agency_info", response_model=ListModel)
    async def agency_info(name: str, page=0, page_size=10):
        NSDI_APP_KEY = app.config["SETTINGS"]["nsdi_key"]
        result = get_agency_info(
            auth_key=NSDI_APP_KEY,
            name=name,
            page=page,
            page_size=page_size,
        )
        #
        if not result:
            raise HTTPException(status_code=500, detail="NSDI API error.")

        return ListModel(
            data=result["field"],
            info={
                "page": page,
                "page_size": page_size,
                "count": int(result["totalCount"]),
            },
        )
