import logging
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%H:%M:%S",
            handlers=[
                logging.FileHandler("autorecon.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AutoRecon")

    def info(self, message):
        print(f"{Fore.BLUE}[*]{Style.RESET_ALL} {message}")
        self.logger.info(message)

    def success(self, message):
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {message}")
        self.logger.info(f"SUCCESS: {message}")

    def warning(self, message):
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {message}")
        self.logger.warning(message)

    def error(self, message):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} {message}")
        self.logger.error(message)

logger = Logger()
