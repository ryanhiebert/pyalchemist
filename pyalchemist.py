"""Recipe builder for transferring data between types."""


class Alchemist:
    """
    Runs a series of transmutations to return a new object.
    """

    def __init__(self, cls=None):
        self.cls = cls
        self.transmutations = []

    def transmutation(self, *args, **kwargs):
        """
        A decorator used to create and add a transmutation.
        """
        def _decorator(callable):
            transmutation = Transmutation(callable, *args, **kwargs)
            self.add_transmutation(transmutation)
            return transmutation

        return _decorator

    def add_transmutation(self, transmutation):
        """
        Safely transmute the designated field from src to dst.
        """
        self.transmutations.append(transmutation)

    def transmute(self, src, cls=None):
        if cls is not None:
            self.cls = cls

        properties = {}
        for transmutation in self.transmutations:
            properties.update(transmutation(src))

        return self.cls(**properties)


class Transmutation:
    """
    A step that an alchemist takes.
    """

    def __init__(self, callable, src_fields=None, dst_fields=None):
        self.callable = callable
        self.src_fields = src_fields
        self.dst_fields = dst_fields

    def __call__(self, src):
        return {}


