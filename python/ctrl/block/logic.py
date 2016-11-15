import numpy
import math

from .. import block

# Blocks

class Compare(block.BufferBlock):

    def __init__(self, abs = False, threshold = 0, *vars, **kwargs):
        """
        Wrapper for state-space model as a Block
        """

        self.abs = abs
        self.threshold = threshold

        super().__init__(*vars, **kwargs)

    def write(self, *values):

        if self.abs:
            test = math.fabs(values[1] - values[0]) <= self.threshold
        else:
            test = values[1] - values[0] >= self.threshold

        if test:
            self.buffer = (1, )
        else:
            self.buffer = (0, )

class Trigger(block.BufferBlock):

    def __init__(self, threshold = 0, state = False, *vars, **kwargs):
        """
        Wrapper for state-space model as a Block
        """

        self.threshold = threshold
        self.state = state

        super().__init__(*vars, **kwargs)

    def set(self, **kwargs):
        
        if 'threshold' in kwargs:
            self.state = kwargs.pop('threshold')
            
        if 'state' in kwargs:
            self.state = kwargs.pop('state')

        super().set(**kwargs)

    def reset(self):

        self.state = False
    
    def write(self, *values):

        if values[0] >= self.threshold:
            self.state = True
            
        if self.state:
            self.buffer = values[1:]
        else:
            self.buffer = tuple((len(values)-1)*[0])