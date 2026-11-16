"""
Реализуйте ProtectedMessageProxy.

Proxy должен предоставлять интерфейс BaseMessage, проверять AccessPolicy
и делегировать render() реальному объекту только при наличии доступа.
"""
from interfaces import BaseMessage
from security.access_policy import AccessPolicy,UserContext

class ProtectedMessageProxy(BaseMessage):

    def __init__(self,message : BaseMessage, access_policy: AccessPolicy, user_context: UserContext) -> None:
        self._message = message
        self._access_policy= access_policy
        self._user_context = user_context

    def render(self) -> str:
        if self._access_policy.is_allowed(self._user_context):
            return self._message.render()
        else:
            raise PermissionError(self._user_context.username)