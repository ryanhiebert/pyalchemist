"""Recipe builder for transferring data between types."""


class Alchemist:
    """
    Look up and perform the correct Transmutation.
    """

    def __init__(self, cls=None):
        self.cls = cls
        self.transmutations = {}

    def transmutation(self, Src, Dst):
        """
        Decorate a transmutation to add.
        """
        def _decorator(transmutation):
            self.add_transmutation(Src, Dst, transmutation)

        return _decorator

    def add_transmutation(self, Src, Dst, transmutation):
        """
        Add a transmutation to the alchemist's arsenal.

        src and dst are classes that this transmutation works on.
        """
        self.transmutations[Dst][Src] = transmutation

    def transmute(src, Dst):
        """
        Find and perform the correct transmutation.
        """
        Src = type(src)
        try:
            self.transmutations[Dst][Src](src, Dst)
        except KeyError:
            raise KeyError(
                'No transmutation found from {} to {}'.format(
                    Src.__name__, Dst.__name__))


class Transmutation:
    """
    A series of rituals that transform an object between types.
    """
    def __init__(self):
        self.rituals = []

    def ritual(self, *args, **kwargs):
        def _decorator(callable):
            ritual = Ritual(callable, *args, **kwargs)
            self.rituals.append(ritual)
            return ritual

    def transmute(self, src, Dst):
        """Run all the rituals in this transmutation"""
        properties = {}

        for ritual in self.rituals:
            properties.update(ritual(src))

        return Dst(**properties)


class Ritual:
    """
    A step in a transmutation.
    """

    def __init__(self, callable, src_fields=None, dst_fields=None):
        self.callable = callable
        self.src_fields = src_fields
        self.dst_fields = dst_fields

    def __call__(self, src):
        dst = SafeObject(self.dst_fields)
        self.callable(src, dst)
        return dst.dict


class SafeObject:
    """
    An mutable object, that can restrict access to given attributes.
    """

    def __init__(self, allowed_fields=None):
        object.__setattr__(self, 'allowed_fields', allowed_fields)
        object.__setattr__(self, 'dict', {})

    def __getattr__(self, name):
        try:
            return self.dict[name]
        except KeyError:
            raise AttributeError(
                'SafeObject({}) has no attribute {}'.format(
                    repr(self.allowed_fields), name))

    def __setattr__(self, name, value):
        if self.allowed_fields is None or name in self.allowed_fields:
            self.dict[name] = value
        else:
            raise AttributeError('Setting \'{}\' attribute not allowed')

    def __delattr__(self, name):
        try:
            del self.dict[name]
        except KeyError:
            raise AttributeError(name)


