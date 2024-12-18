from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Базовые настройки приложения.
    """

    model_config = SettingsConfigDict(env_file='src/.env', env_file_encoding='utf-8', extra='ignore')

    # Common
    APP: str = 'main:app'
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    SWAGGER_TITLE: str = 'ООО УК Управдом'
    APP_VERSION: str = '0.0.0'
    ROOT_PATH: str = ''
    IS_DEBUG: bool = False

    # DB
    SQL_DSN: str = 'postgresql+asyncpg://localhost/postgres'
    SQL_SCHEMA: str = 'public'

    # Auth
    AUTH_URL: str = ''  # TODO добавить авторизацию

    DEBTOR_MESSAGE_TEMPLATE: str = """
                                                                      кому: {}
                                                                            {}
                                                                      от: ООО УК Управдом
                                                                      
                                Уведомление о просроченной задолженности.
                                
    Уважаемый(ая) {}, ООО УК Управдом сообщает о наличии у Вас задолженности в общем размере {}:
    {}
    
    В случае не погашения задолженности в течение 30-ти дней, управляющая компания оставляет за собой право отключить
    Вашу квартиру от коммуникаций и обратиться в мировой суд в заявлением о взыскании с Вас коммунальной задолжености.
    
    К сожалению, в такой ситуации до момента поступления денежных средств на счет управляющей компании, вы останетесь
    без электричества, воды и отопления.
    
    Надеемся на Ваше понимание и своевременную оплату.
    
    С уважением,
    директор ООО УК Управдом
    Курицын Александр Всеволодович
    """


app_settings = AppSettings()
