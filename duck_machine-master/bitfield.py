"""                # Bit fields
Cis 211 project 7
Author: Anne Glickenhaus
A bit field is a range of binary digits within an
unsigned integer. Bit 0 is the low-order bit,
with value 1 = 2^0. Bit 31 is the high-order bit,
with value 2^31. 

A bitfield object is an aid to encoding and decoding 
instructions by packing and unpacking parts of the 
instruction in different fields within individual 
instruction words. 

Note that we are treating Python integers as if they 
were 32-bit unsigned integers.  They aren't ... Python 
actually uses a variable length signed integer
representation, but we ignore that because we are trying
to simulate a machine-level representation. 
"""

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

WORD_SIZE = 32 


class BitField(object):
    """A BitField object handles insertion and 
    extraction of one field within an integer.
    """
    def __init__(self, from_bit: int, to_bit: int):
        self.from_bit = from_bit
        self.to_bit = to_bit

        self.field_width = 1 + self.to_bit - self.from_bit

        self.mask = self._makemask(self.field_width)


    def _makemask(self, field_w: int) -> int:
        '''Makes a binary number of all '1's the length of the field width,
        returns the integer of 1's.
        '''
        mask = 0
        for bit in range(field_w):
            mask = (mask << 1) + 1

        return mask


    def insert(self, field_val: int, word: int) -> int:
        '''Shifts the mask to desired location to clear those bits,
        inserts field value into the cleared spot. Returns word with field value
        inserted.
        '''
        eraser = ~ (self.mask << self.from_bit)
        mask_word = word & eraser

        inserted = mask_word | ((self.mask & field_val) << self.from_bit)

        return inserted

    def extract(self, word: int) -> int:
        '''Shifts word to the right until desired bit is the farthest right.
        Use mask to clear out everything unwanted. Returns extracted integer.
        '''
        val_out = word >> self.from_bit
        original_field = val_out & self.mask

        return original_field

    def extract_signed(self, word: int) -> int:
        '''If far left bit is 0, integer is positive, if far left bit is 1,
        then the value of the integer is negative. Return the signed value.
        '''
        extracted_f = self.extract(word)

        return sign_extend(extracted_f, self.field_width)


def sign_extend(field: int, width: int) -> int:
    """Interpret field as a signed integer with width bits.
    If the sign bit is zero, it is positive.  If the sign bit
    is negative, the result is sign-extended to be a negative
    integer in Python.
    width must be 2 or greater. field must fit in width bits.
    """
    log.debug("Sign extending {} ({}) in field of {} bits".format(field, bin(field), width))
    assert width > 1
    assert field >= 0 and field < 1 << (width + 1)
    sign_bit = 1 << (width - 1) # will have form 1000... for width of field
    mask = sign_bit - 1         # will have form 0111... for width of field
    if (field & sign_bit):
        # It's negative; sign extend it
        log.debug("Complementing by subtracting 2^{}={}".format(width-1,sign_bit))
        extended = (field & mask) - sign_bit
        log.debug("Should return {} ({})".format(extended, bin(extended)))
        return extended
    else:
        return field

