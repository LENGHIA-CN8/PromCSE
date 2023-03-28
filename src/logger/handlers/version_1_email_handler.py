from logging.handlers import SMTPHandler
from logging import LogRecord
import smtplib
from datetime import datetime
from typing import Tuple, List, Optional
from logging import ERROR, WARNING, INFO, DEBUG
from .base_handler_config import BaseHandlerConfig


class EmailHandlerVersion1(SMTPHandler):
    """
    Class for Handle log record via sending email version 1
    """
    def _get_message(self, record: LogRecord) -> str:
        """
        Get string representation of message
        :param record: log record
        :return: string represent the content of the message
        """
        current_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_subject: str = f"{current_time}   " + self.getSubject(record=record)
        msg_from: str = self.fromaddr
        msg_to: str = ",".join(self.toaddrs)
        msg_content: str = self.format(record)
        msg: str = f"From: {msg_from}\r\nTo: {msg_to}\r\nSubject: {msg_subject}\r\n\r\n{msg_content}"
        return msg

    def _send_message(self, message: str):
        """
        Send message via email
        :param message: string
        :return:
        """
        smtp: smtplib.SMTP = smtplib.SMTP(self.mailhost, self.mailport)
        smtp.starttls()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.fromaddr, self.toaddrs, message)
        smtp.quit()

    def emit(self, record: LogRecord):
        """
        Handle log record
        :param record: log record
        :return:
        """
        try:
            message: str = self._get_message(record=record)
            self._send_message(message=message)
        except Exception as ex:
            print(f"EXCEPTION WHILE PROCESSING LOG RECORD:")
            print(ex)
            pass


class EmailHandlerVersion1Config(BaseHandlerConfig):
    """
    Config class for handle log records via sending email version 1
    """
    def __init__(self, mail_host: Tuple[str, int], from_address: str, to_addresses: List[str],
                 subject: str, credentials: Tuple[str, str],
                 logger_level: Optional[int] = None, format_string: Optional[str] = None):
        """
        Init method
        :param mail_host: mail host, mail port
        :param from_address: email address to send message from
        :param to_addresses: email addresses to send message to
        :param subject: subject of message
        :param credentials: email address, password
        :param logger_level: logger level
        :param format_string: format string
        """
        self.mail_host = mail_host
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.subject = subject
        self.credentials = credentials
        self.logger_level = logger_level
        self.format_string = format_string

    @property
    def mail_host(self) -> Tuple[str, int]:
        return self._mail_host

    @mail_host.setter
    def mail_host(self, mail_host: Tuple[str, int]):
        assert isinstance(mail_host, tuple) and len(mail_host) == 2
        assert isinstance(mail_host[0], str) and isinstance(mail_host[1], int)
        self._mail_host: Tuple[str, int] = mail_host

    @property
    def from_address(self) -> str:
        return self._from_address

    @from_address.setter
    def from_address(self, from_address: str):
        assert isinstance(from_address, str)
        self._from_address: str = from_address

    @property
    def to_addresses(self) -> List[str]:
        return self._to_addresses

    @to_addresses.setter
    def to_addresses(self, to_addresses: List[str]):
        assert isinstance(to_addresses, list)
        assert all(map(lambda x: isinstance(x, str), to_addresses))
        self._to_addresses: List[str] = to_addresses

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject: str):
        assert isinstance(subject, str)
        self._subject: str = subject

    @property
    def credentials(self) -> Tuple[str, str]:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: Tuple[str, str]):
        assert isinstance(credentials, tuple) and len(credentials) == 2
        assert isinstance(credentials[0], str) and isinstance(credentials[1], str)
        self._credentials: Tuple[str, str] = credentials

    @property
    def logger_level(self) -> int:
        return self._logger_level

    @logger_level.setter
    def logger_level(self, logger_level: Optional[int]):
        if logger_level is None:
            logger_level = DEBUG
        else:
            assert isinstance(logger_level, int)
            if logger_level not in {ERROR, WARNING, DEBUG, INFO}:
                print(f"Invalid logger level {logger_level}")
                logger_level = DEBUG
        self._logger_level: int = logger_level

    @property
    def format_string(self) -> str:
        return self._format_string

    @format_string.setter
    def format_string(self, format_string: Optional[str]):
        if format_string is None:
            format_string = '%(levelname)s   %(asctime)s   %(message)s'
        else:
            assert isinstance(format_string, str)
        self._format_string: str = format_string

