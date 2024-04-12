import logging
import requests


class FabCon:
    def __init__(self, config):
        self.printer = printer = config.get_printer()
        self.api_ip = config.get('ip')
        self.api_key = config.get('key', '')
        self.machine = config.get('machine')
        self.in_use = False


        self.printer.register_event_handler("action:cancel",
                                            self._handle_free)
        self.printer.register_event_handler("action:start",
                                            self._handle_check)
        self.printer.register_event_handler("action:complete",
                                            self._handle_free)
        self.printer.register_event_handler("klippy:ready",
                                            self._handle_startup)

    def _handle_check(self):
        logging.info("FABACCESS CHECK")
        try: 
            req = requests.get("http://" + self.api_ip + "/in_use/" + self.machine, timeout=1)
            if req.text == "in_use":
                logging.info("FABACCESS Machine in Use, Proceeding")
                self.in_use = True 
            elif req.text == "free":
                logging.info("FABACCESS Machine not registered to User, Canceling")
                self.printer.invoke_shutdown("FABACCESS Machine not registered to User")
            elif req.text == "disabled":
                logging.info("FABACCESS Machine Blocked, Canceling")
                self.printer.invoke_shutdown("FABACCESS Machine Blocked")
            elif req.text == "blocked":
                logging.info("FABACCESS Machine Disabled, Canceling")
                self.printer.invoke_shutdown("FABACCESS Machine Disabled")
        except:
            logging.warning("FABACCESS ERROR")

    def _handle_free(self):
        logging.info("FABACCESS FREE")
        try: 
            req = requests.get("http://" + self.api_ip + "/free/" + self.machine, timeout=1)
            logging.info("FABACCESS Machine freed")
            self.in_use = False
        except:
            logging.warning("FABACCESS ERROR")

    def _handle_startup(self):
        logging.info("FABACCESS LOADED")

    def get_status(self, eventtime):
        data = {
            'in_use': self.in_use
        }
        return data


def load_config(config):
    return FabCon(config)