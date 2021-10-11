def main(app):
    @app.post("/crontab")
    def crontab():
        # TODO:
        pass

    @app.get("/crontab")
    def crontabs():
        # TODO:
        pass

    @app.get("/crontab/{crontab_id}")
    def get_crontab(crontab_id: str):
        # TODO:
        pass

    @app.get("/health")
    def health_check():
        return {"status": "OK"}
