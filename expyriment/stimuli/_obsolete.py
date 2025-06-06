"""
Obsolete stimuli

Calls are merely defined to give user appropriate error feedback

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

class Dot(object):
    """OBSOLETE CLASS: Please use Circle!"""

    def __init__(self, radius=None, colour=None, position=None):
        """OBSOLETE CLASS: Please use Circle!

        """

        raise DeprecationWarning("Dot is an obsolete class. Please use Circle!")


class Frame(object):
    """OBSOLETE CLASS: Please use Rectangle!"""

    def __init__(self, size=None, position=None, frame_line_width=None,
                 colour=None, anti_aliasing=None, line_width=None):
        """OBSOLETE CLASS: Please use Rectangle with a line_width > 0!

        """
        raise DeprecationWarning("Frame is an obsolete class. Please use Rectangle with a line_width > 0!")
