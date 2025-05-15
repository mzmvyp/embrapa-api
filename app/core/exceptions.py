# 10. app/core/exceptions.py
class EmbrapaException(Exception):
    """Exceção base para erros específicos da aplicação Embrapa."""
    pass

class WebScrapingError(EmbrapaException):
    """Exceção para erros durante o web scraping."""
    pass

class DataProcessingError(EmbrapaException):
    """Exceção para erros no processamento de dados."""
    pass