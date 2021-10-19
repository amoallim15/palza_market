from fastapi import Body
from src.models.report import (
    CreateReportModel,
    UpdateReportModel,
)


def main(app):
    @app.get("/report")
    def reports():
        # TODO: get reports from the database
        pass

    @app.get("/report/{report_id}")
    def get_report(report_id: str):
        # TODO:
        pass

    @app.post("/report")
    def create_report(report: CreateReportModel = Body(...)):
        # TODO: post new report
        pass

    @app.put("/report/{report_id}")
    def update_report(report_id: str, report: UpdateReportModel = Body(...)):
        # TODO: update report
        pass

    @app.delete("/report/{report_id}")
    def delete_report(report_id: str):
        # TODO: delete report
        pass
