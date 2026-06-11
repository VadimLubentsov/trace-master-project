import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "API Gateway")

    SSO_SERVICE_URL: str = os.getenv(
        "SSO_SERVICE_URL",
        "http://127.0.0.1:8002",
    )

    PRODUCT_SERVICE_URL: str = os.getenv(
        "PRODUCT_SERVICE_URL",
        "http://127.0.0.1:8001",
    )


settings = Settings()
