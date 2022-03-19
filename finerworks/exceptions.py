class FinerworksError(Exception):
    """Basic exception raised for Finerworks formatting errors."""
    def __init__(self, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "An unknown error occured with the finerworks API or data formatting."
        super(FinerworksError, self).__init__(msg)