from src.models.api_models import Report
from uuid import UUID


def main(app):
    @app.get("/report")
    def reports():
        # TODO: get reports from the database
        pass

    @app.post("/report")
    def create_report():
        # TODO: post new report
        pass

    @app.put("/report/{report_id}")
    def update_report(report_id: UUID, report: Report):
        # TODO: update report
        pass

    @app.delete("/report/{report_id}")
    def delete_report(report_id: UUID, report: Report):
        # TODO: delete report
        pass
