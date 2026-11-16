import base64
from datetime import datetime

from decorators.message_decorator import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    MessageDecorator,
    SignatureDecorator,
)
from interfaces import BaseMessage
from messages import Message


def test_message_decorator_returns_same_text() -> None:
    message = MessageDecorator(Message("Текст"))
    assert message.render() == "Текст"


def test_decorator_is_base_message() -> None:
    message = HeaderDecorator(Message("Текст"), "Заголовок")
    assert isinstance(message, BaseMessage)


def test_header_decorator() -> None:
    message = HeaderDecorator(Message("Текст"), "Заголовок")
    assert message.render() == "Заголовок\nТекст"


def test_signature_decorator() -> None:
    message = SignatureDecorator(Message("Текст"), "Савин Егор")
    assert message.render() == "Текст\n\nС уважением Савин Егор"


def test_date_decorator() -> None:
    message = DateDecorator(Message("Текст"), datetime(2026, 12, 31))
    assert message.render() == "Текст\nОтправлено 2026-12-31 00:00:00"


def test_base64_decorator() -> None:
    message = Base64Decorator(Message("Текст"))
    assert message.render() == "0KLQtdC60YHRgg=="


def test_header_and_signature_together() -> None:
    message = SignatureDecorator(HeaderDecorator(Message("Текст"), "Заголовок"), "Савин Егор")
    assert message.render() == "Заголовок\nТекст\n\nС уважением Савин Егор"


def test_all_decorators_together() -> None:
    message = Message("Текст")
    message = HeaderDecorator(message, "Заголовок")
    message = SignatureDecorator(message, "Савин Егор")
    message = DateDecorator(message, datetime(2026, 12, 31))
    message = Base64Decorator(message)

    decoded = base64.b64decode(message.render()).decode("utf-8")
    assert decoded == "Заголовок\nТекст\n\nС уважением Савин Егор\nОтправлено 2026-12-31 00:00:00"


