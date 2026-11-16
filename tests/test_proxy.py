import pytest

from decorators.message_decorator import HeaderDecorator
from messages import Message
from proxies.protected_message_proxy import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def test_proxy_allows_user_with_role() -> None:
    message = Message("Текст")
    policy = AccessPolicy("reader")
    alice = UserContext.of("alice", "reader")

    proxy = ProtectedMessageProxy(message, policy, alice)

    assert proxy.render() == "Текст"


def test_proxy_denies_user_without_role() -> None:
    message = Message("Текст")
    policy = AccessPolicy("reader")
    bob = UserContext.of("bob", "guest")

    proxy = ProtectedMessageProxy(message, policy, bob)

    with pytest.raises(PermissionError):
        proxy.render()


def test_proxy_does_not_change_text() -> None:
    message = HeaderDecorator(Message("Текст"), "Заголовок")
    policy = AccessPolicy("reader")
    alice = UserContext.of("alice", "reader")

    proxy = ProtectedMessageProxy(message, policy, alice)

    assert proxy.render() == message.render()
