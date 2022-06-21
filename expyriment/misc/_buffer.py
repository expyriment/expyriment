"""
An event buffer.

This module contains a class implementing an event buffer.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from ._clock import Clock
from .. import _internals


class Buffer(object):
    """A class implementing a general event buffer."""

    def __init__(self, name="Buffer", clock=None):
        """Create an event buffer.

        Parameters
        ----------
        name : str
            the name of the buffer
        clock : expyriment.Clock object (optional)
            an experimental clock

        """

        self._name = name
        if clock is not None:
            self._clock = clock
        else:
            if _internals.active_exp.is_initialized:
                self._clock = _internals.active_exp.clock
            else:
                self._clock = Clock()
        self._memory = []

    @property
    def name(self):
        """Getter for name"""
        return self._name

    @property
    def clock(self):
        """Getter for clock"""
        return self._clock

    @property
    def memory(self):
        """Getter for memory [list of tuples (code, rt)]"""
        return self._memory

    def add_event(self, event):
        """Add an event to the buffer.

        Parameters
        ----------
        event : anything
            the event to add

        """

        item = (event, self._clock.time)
        self._memory.append(item)

    def add_events(self, events):
        """Add a list of events to the buffer.

        All events get the same time stamp!

        Parameters
        ----------
        events : list
            the event list to add

        """
        ts = [self._clock.time] * len(events)
        self._memory.extend(list(zip(events, ts)))

    def get_size(self):
        """Return the number of elements in the buffer.
        
        Returns
        -------
        size : int
            the size of the buffer
    
        """

        return len(self._memory)

    def get_element(self, position):
        """Get an element (code, rt) from the buffer. 

        Parameters
        ----------
        position : int
            the position to get the element from
            
        Returns
        -------
        element : (anything, float)
            The element to get from the buffer
            
        """

        if position < len(self._memory) and position >= 0:
            element = self._memory[position]
        else:
            element = (0, 0)
        return element

    def clear(self):
        """Clear the buffer."""

        self._memory = []

    def get_last_event(self):
        """Get the last event (code, rt) in the buffer.
        
        Returns
        -------
        element : (anything, float)
            the last element of the buffer
            
        """

        if len(self._memory) > 0:
            element = self._memory[-1]
        else:
            element = [0, 0]
        return element

    def get_whole_buffer(self):
        """Get a copy of the buffer.
        
        Returns
        -------
        copy : list
            the copy of the buffer
            
        """

        bcopy = self._memory[:]
        return bcopy


class ByteBuffer(Buffer):
    """A class implementing a buffer for bytes.

    The ByteBuffer class is also used for the input_histoy of serial and
    parallel ports.

    """

    def __init__(self, name="ByteBuffer", clock=None):
        """Create a buffer for bytes.

        Parameters
        ----------
        name : str
            the name of the buffer
        clock : expyriment.Clock object (optional)
            an experimental clock

        """

        Buffer.__init__(self, name, clock)

    def check_set(self, search_byte, search_start_position=0):
        """
        Check if bits are set in buffer bytes and return position.

        Parameters
        ----------
        search_byte : int
            the byte to search for
        search_start_position : int (optional)
            position to start search from (int)
        
        Returns
        -------
        position : int
            the position of element with set bits
            
        """

        found_pos = 0
        pos = search_start_position
        for x in range(pos, len(self._memory)):
            elem = self._memory[x]
            # OR: at least one of the bits is set
            if (elem[0] & search_byte) > 0:
                found_pos = x
        return found_pos

    def check_unset(self, search_byte, search_start_position=0):
        """
        Check if bits are NOT set in buffer bytes and return position.

        Parameters
        ----------
        search_byte : int
            the byte to search for
        search_start_position : int (optional)
            position to start search from
            
        Returns
        -------
        position : int
            the position of element with unset bits

        """

        found_pos = 0
        pos = search_start_position
        for x in range(pos, len(self._memory)):
            elem = self._memory[x]
            # OR: at least one of the bits is set
            if (elem[0] ^ 255) & search_byte:
                found_pos = x
        return found_pos

    def check_value(self, value, search_start_position=0):
        """
        Check if value is in buffer bytes and return the position.

        Parameters
        ----------
        value : int
            the value to check
        search_start_position : int (optional)
            position to start search from
            
        Returns
        -------
        position : int
            the position of element with value

        """

        found_pos = 0
        pos = search_start_position
        for x in range(pos, len(self._memory)):
            elem = self._memory[x]
            if elem[0] == value:
                found_pos = x
        return found_pos
