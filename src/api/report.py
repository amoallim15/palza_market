from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserRole

from src.models.report import (
    ReportModel,
    UpdateReportModel,
)


def main(app):
    @app.get("/report", response_model=ListModel)
    async def reports(
        page: int = Query(0, ge=0), current_user=Depends(app.current_user)
    ):
        _filter = {}
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            _filter = { user_id: current_user.id }
        #
        page_size = app.config["APP"]["page_size"]
        #
        cursor = app.db["reports"].find(_filter).skip(page * page_size).limit(page_size)
        count = await app.db["reports"].count_documents({})
        data_list = []
        #
        async for report in cursor:
            data_list.append(ReportModel(**report))
        #
        return ListModel(page=page, count=count, data=data_list)

    @app.get("/report/{report_id}", response_model=ReportModel)
    async def get_report(report_id: str, current_user=Depends(app.current_user)):
        data = await app.db["reports"].find_one({"_id": report_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        #
        if (
            current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]
            or current_user.id != data["user_id"]
        ):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        return ReportModel(**data)

    @app.post("/report", response_model=ReportModel)
    async def create_report(
        report: ReportModel = Body(...), current_user=Depends(app.current_user)
    ):
        realstate = app.db["realstates"].find_one({"realstate_id": report.realstate_id})
        if not realstate:
            raise HTTPException(status_code=400, detail="Realstate does not exist.")
        #
        report = jsonable_encoder(report)
        # 
        report["user_id"] = current_user.id
        # 
        result = await app.db["reports"].insert_one(report)
        data = await app.db["reports"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        #
        return ReportModel(**data)

    @app.put("/report/{report_id}", response_model=ReportModel)
    async def update_report(
        report_id: str,
        report: UpdateReportModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        data = await app.db["reports"].find_one({"_id": report_id})
        if not data:
            raise HTTPException(status_code=404, detail="Report not found.")
        # 
        if (
            current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]
            or current_user.id != data["user_id"]
        ):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        report = jsonable_encoder(report)
        await app.db["reports"].update_one({"_id": report_id}, {"$set": report})
        data = await app.db["reports"].find_one({"_id": report_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        #
        return ReportModel(**data)

    @app.delete("/report/{report_id}", response_model=SuccessModel)
    async def delete_report(
        report_id: str,
        current_user=Depends(app.current_user),
    ):
        data = await app.db["reports"].find_one(
            {"_id": report_id}, current_user=Depends(app.current_user)
        )
        if not data:
            raise HTTPException(status_code=404, detail="Report not found.")
        if (
            current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]
            or current_user.id != data["user_id"]
        ):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["reports"].delete_one({"_id": report_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Report not found.")
