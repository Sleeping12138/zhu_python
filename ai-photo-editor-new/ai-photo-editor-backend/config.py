from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 数据库配置
    DB_CONFIG: dict = {
        'host': '121.37.27.174',
        'user': 'ai_user',
        'password': 'yishou@666',
        'database': 'world'
    }

    # 后端IP
    BASE_URL: str = 'http://14.103.147.199'

    # 图片处理端口号
    PROCESS_SERVICE_PORT: str = "5084"
    VIRTUAL_TRY_SERVICE_PORT: str = "5136"

    # OBS 配置
    OBS_ACCESS_KEY_ID: str = "EULIXLKJQLUS62GPNIAX"
    OBS_SECRET_ACCESS_KEY: str = "vmoTDJVUOXVtwt8pwh5LQ6LnE2bJPDtxid7biimK"
    OBS_SERVER: str = "https://obs.cn-south-1.myhuaweicloud.com"


settings = Settings()
