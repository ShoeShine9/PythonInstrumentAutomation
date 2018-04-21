class WrongInstrumentError(Exception):
    """The wrong instrument is connected

    A connection was successfuly established, and the instrument responded
    to a request to identify itself, but the ID recieved was wrong.
    Probably the instrument at the given VISA identifier is not the one
    you wanted.
    """
    pass


class InstrumentNotResponding(Exception):
    print("Specified instrument is not responding")


class IncorrectAddress(Exception):
    def __init__(self, inst_name):
        print("the visa resource address specified is for {}".format(inst_name))


class InvalidValue(Exception):
    def __init__(self, value):
        print("the value {} is not valid for this command".format(value))