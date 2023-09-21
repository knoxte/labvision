
class NotImageError(Exception):
    """NotImageError

    This exception is raised when something which is not the correct
    depth of array to be an image is sent to a function.

    Parameters
    ----------
    Exception : _type_
        Designed to catch passing wrong thing to image functions
    """
    def __init__(self):
        Error_msg = "This error indicates the array passed is not correct shape for an image. Check its not an empty image as opencv passes this silently. Check it has correct dimensions"
        super().__init__(self, Error_msg)

class NotBinaryImageError(Exception):
    """NotBinaryImageError

    Parameters
    ----------
    Exception : _type_
        _description_
    """
    def __init__(self):
        Error_msg = "This error indicates the array passed is not a binary image as expected by the function"
        super().__init__(self, Error_msg)

class NotRGBImageError(Exception):
    """NotBinaryImageError

    Parameters
    ----------
    Exception : _type_
        _description_
    """
    def __init__(self):
        Error_msg = "This error indicates the array passed is not an RGB image as expected by the function"
        super().__init__(self, Error_msg)

class NotGrayscaleImageError(Exception):
    """NotBinaryImageError

    Parameters
    ----------
    Exception : _type_
        _description_
    """
    def __init__(self):
        Error_msg = "This error indicates the array passed is not a grayscale image as expected by the function"
        super().__init__(self, Error_msg)