
class KintonError(Exception):
    pass


class FieldDoesNotExists(KintonError):
    pass


class ObjectDoesNotExists(KintonError):
    pass


class MultipleObjectsReturned(KintonError):
    pass
