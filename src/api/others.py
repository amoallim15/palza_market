from src.core.model import SuccessModel


def main(app):
    #
    @app.get("/health", response_model=SuccessModel)
    async def info():
        return SuccessModel(detail="OK.")
