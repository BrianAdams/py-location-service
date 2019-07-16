class RecoverableException(Exception):
    pass

class UnRecoverableException(Exception):
    pass

class PermissionDenied(UnRecoverableException):
    pass

class QuotaLimit(RecoverableException):
    pass

class InvalidRequest(UnRecoverableException):
    pass

class ThirdPartyError(RecoverableException):
    pass
