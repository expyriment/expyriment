"""
A touchscreen button box.

This module contains a class implementing a text input box for user input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import defaults
import expyriment
from _input_output import Input


class TextInput(Input):
    """A class implementing a text input box."""

    def __init__(self, button_fields):
        """Create a touchscreen button box.

		TODO 

        """
		
		self._button_fields = button_fields

    def add_button_field(self, button_field):
		if not isinstance(button_field, expyriment.stimuli._visual.Visual):
		   raise TypeError("Button_field have to be visual Expyriment stimulus")

		background_stimulus.__class__.__base__ in \
            [, expyriment.stimuli.Shape]:


	def present(self, background_stimulus):
        """

		TODO 

		"""
		
		pass

