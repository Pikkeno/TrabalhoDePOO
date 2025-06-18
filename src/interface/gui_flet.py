import os
import sys

if __package__ is None:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from src.views.main_view import flet_main
from src.utils.logger import logger

logger.info("Módulo Flet carregado")
