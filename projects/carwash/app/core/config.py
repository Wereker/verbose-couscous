from pydantic import BaseModel, Field
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    # host: str = "127.0.0.1"
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    profile: str = "/profile"
    brands: str = "/brands"
    services: str = "/services"
    cars: str = "/cars"
    roles: str = "/roles"
    users: str = "/users"
    role_users: str = "/role-users"
    customer_cars: str = "/customer-cars"
    orders: str = "/orders"
    order_services: str = "/order-services"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # api/v1/auth/login
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        # return path[1:]
        return path.removeprefix("/")


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str

class AuthConfig(BaseModel):
    secret_key: str
    refresh_secret_key: str
    algorithm: str
    access_token_expire_minutes: int = Field(..., alias="access_token_expire_minutes")
    refresh_token_expire_minutes: int = Field(..., alias="refresh_token_expire_minutes")


class RedisConfig(BaseModel):
    host: str
    port: int
    expire_seconds: int


class CeleryConfig(BaseModel):
    smtp_hostname: str = Field(..., alias="smtp_hostname")
    smtp_port: str = Field(..., alias="smtp_port")
    email_sender: str = Field(..., alias="email_sender")
    email_username: str = Field(..., alias="email_username")
    email_password: str = Field(..., alias="email_password")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    access_token: AccessToken
    auth: AuthConfig
    redis: RedisConfig
    celery: CeleryConfig


settings = Settings()
