from decorators.message_decorator import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    SignatureDecorator,
)
from messages import Message
from proxies.protected_message_proxy import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def main() -> None:

    message = Message(
        "Рады предложить вам должность младшего Python-разработчика. "
    )
    print("Исходное сообщение:")
    print(message.render())
    print()

    decorated = HeaderDecorator(message, "Оффер")
    decorated = SignatureDecorator(decorated, "Анна Смирнова, HR-менеджер")
    decorated = DateDecorator(decorated)
    print("С декораторами:")
    print(decorated.render())
    print()

    encoded = Base64Decorator(decorated)
    print("В Base64:")
    print(encoded.render())
    print()

    policy = AccessPolicy("hr")
    anna = UserContext.of("anna", "hr")
    proxy = ProtectedMessageProxy(decorated, policy, anna)
    print("Proxy, пользователь anna (роль hr):")
    print(proxy.render())
    print()

    ivan = UserContext.of("egor", "developer")
    proxy = ProtectedMessageProxy(decorated, policy, ivan)
    print("Proxy, пользователь egor (роль developer):")
    try:
        print(proxy.render())
    except PermissionError as error:
        print("Доступ запрещён:", error)


if __name__ == "__main__":
    main()
