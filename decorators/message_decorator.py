"""
Базовый Decorator и конкретные декораторы необходимо реализовать самостоятельно.

Подсказка: все декораторы должны удовлетворять интерфейсу BaseMessage и
работать с другим объектом BaseMessage через композицию.
"""
import base64

from interfaces import BaseMessage
from datetime import datetime

class MessageDecorator(BaseMessage):
    def __init__(self, message: BaseMessage) -> None:
        self._message=message

    def render(self) -> str:
        return self._message.render()


class HeaderDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, header: str) -> None:
        super().__init__(message)
        self._header= header

    def render(self) -> str:
        return f"{self._header}\n{super().render()}"


class SignatureDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, signature : str):
        super().__init__(message)
        self._signature = signature

    def render(self) -> str:
        return f"{super().render()}\n\nС уважением {self._signature}"


class DateDecorator(MessageDecorator):
    def __init__(self,message : BaseMessage, date: datetime | None = None):
        super().__init__(message)
        self._date = date or datetime.now()

    def render(self)-> str:
        return f"{super().render()}\nОтправлено {self._date}"


class Base64Decorator(MessageDecorator):
    def render(self)-> str:
        text = super().render()
        encoded_bytes= text.encode("utf-8")
        return base64.b64encode(encoded_bytes).decode("utf-8")