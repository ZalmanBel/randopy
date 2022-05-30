"""Random functions"""
import random
import string  # For generating random strings or digits
import secrets  # For more cryptographically safe functions
from typing import cast, TypeAlias, TypeVar
from collections.abc import Callable, Sequence  # For type annotating

from randopy._first import first_names  # type: ignore
from randopy._last import last_names  # type: ignore

T = TypeVar('T')
Choice: TypeAlias = Callable[[Sequence[T]], T]
randomizer = secrets.SystemRandom()


class WrongLengthError(ValueError):
    """Raised when an integer with a bad length is given"""


def rcint(choice: Choice, length: int = 1, start: int | None = None,
          end: int | None = None, *, check_zero: bool = True,
          as_str: bool = False) -> int | str:
    """Temporary function to take in a choice function"""
    # Raise error if length doesn't match correctly with start or end
    if ((len(str(start)) != length and start is not None)
            or (len(str(end)) != length and end is not None)):
        raise WrongLengthError(f"{start=} or {end=} doesn't match {length=}")
    # Or if length is zero or less
    elif length <= 0:
        raise WrongLengthError(f'invalid length: {length}')

    while True:  # Get values until they line up with start and end correctly
        return_val = ''
        # Get a string of random digits with the correct length
        for i in range(length):
            return_val += choice(string.digits)

        if check_zero and length != 1:
            while True:  # Make sure zero isn't in the beginning
                if return_val[0] == '0':
                    return_val = return_val[1:]
                    return_val += choice(string.digits)
                else:
                    break

        if start is None and end is None:
            break  # Check start and end values
        elif start is None:
            if int(return_val) <= cast(int, end):
                break
        elif end is None:
            if int(return_val) >= start:
                break
        else:
            if start <= int(return_val) <= end:
                break

    if as_str:
        return return_val
    return int(return_val)  # Return as an int because it's a string


def randoint(length: int = 1, start: int | None = None,
             end: int | None = None, *, check_zero: bool = True,
             as_str: bool = False) -> int | str:
    """Function for generating random intergers"""
    return rcint(random.choice, length, start, end,
                 check_zero=check_zero, as_str=as_str)


def cryptoint(length: int = 1, start: int | None = None,
              end: int | None = None, *, check_zero: bool = True,
              as_str: bool = False) -> int | str:
    """Function for generating cryptographically safe and random integers"""
    return rcint(secrets.choice, length, start, end,
                 check_zero=check_zero, as_str=as_str)


def rcfloat(choice: Choice,
            prelength: int = 1,
            postlength: int = 1,
            start: float | None = None,
            end: float | None = None) -> float:
    """Temporary function to take in a choice function"""
    # Raise error is start or end are True or False
    # (because they can be interpreted as integers)
    if any([start is True, start is False, end is True, end is False]):
        raise WrongLengthError(
            f"{start=} or {end=} doesn't match {prelength=} or {postlength=}"
        )
    start = None if start is None else float(start)
    end = None if end is None else float(end)
    # Raise error if prelength doesn't match correctly with start or end
    if ((start is not None
         and len(str(start)[:str(start).find('.')]) != prelength)
            or (end is not None
                and len(str(end)[:str(end).find('.')]) != prelength)):
        raise WrongLengthError(
            f"{start=} or {end=} doesn't match {prelength=}"
        )
    # Or if prelength or postlength is less than or equal to zero
    elif prelength <= 0 or postlength <= 0:
        raise WrongLengthError(f'invalid length {prelength} or {postlength}')
    # Raise error if postlength doesn't match correctly with start or end
    elif ((start is not None
           and len(str(start)[str(start).find('.') + 1:]) != postlength)
          or (end is not None
              and len(str(end)[str(end).find('.') + 1:]) != postlength)):
        raise WrongLengthError(
            f"{start=} or {end=} doesn't match {postlength=}"
        )

    while True:  # Get values until they line up with start and end correctly
        # Get a string of random digits with the correct length
        return_val = (cast(str, rcint(choice, length=prelength,
                                      as_str=True)) + '.' +
                      cast(str, rcint(choice, length=postlength,
                                      check_zero=False, as_str=True)))
        if start is None and not end:
            break  # Check start and end values
        elif start is None:
            if float(return_val) <= cast(float, end):
                break
        elif not end:
            if float(return_val) >= start:
                break
        else:
            if start <= float(return_val) <= cast(float, end):
                break

    return float(return_val)  # Return as a float because it's a string


def randofloat(prelength: int = 1,
               postlength: int = 1,
               start: float | None = None,
               end: float | None = None) -> float:
    """Function for generating random floating point numbers"""
    return rcfloat(random.choice, prelength, postlength, start, end)


def cryptofloat(prelength: int = 1,
                postlength: int = 1,
                start: float | None = None,
                end: float | None = None) -> float:
    """Function for generating cryptographically safe and random
     floating point numbers"""
    return rcfloat(secrets.choice, prelength, postlength, start, end)


def rccomplex(choice: Choice,
              realprelength: int = 1,
              realpostlength: int = 1,
              imagprelength: int = 1,
              imagpostlength: int = 1,
              start: complex | None = None,
              end: complex | None = None) -> complex:
    """Temporary function to take in a choice function"""
    # Check to make sure lengths, start, and end match up
    if start is not None:
        randofloat(prelength=realprelength, postlength=realpostlength,
                   start=start.real)
        randofloat(prelength=imagprelength, postlength=imagpostlength,
                   start=start.imag)
    if end is not None:
        randofloat(prelength=realprelength, postlength=realpostlength,
                   end=end.real)
        randofloat(prelength=imagprelength, postlength=imagpostlength,
                   end=end.imag)

    while True:  # Get values until they line up with start and end correctly
        return_val = complex(rcfloat(choice, realprelength, realpostlength),
                             rcfloat(choice, imagprelength, imagpostlength))
        if start is None and end is None:
            break  # Check start and end values
        elif start is None:
            if (return_val.real <= cast(complex, end).real
                    and return_val.imag <= cast(complex, end).imag):
                break
        elif end is None:
            if return_val.real >= start.real and return_val.imag <= start.imag:
                break
        else:
            if (start.real <= return_val.real <= end.real
                    and start.imag <= return_val.imag <= end.imag):
                break

    return return_val


def randocomplex(realprelength: int = 1,
                 realpostlength: int = 1,
                 imagprelength: int = 1,
                 imagpostlength: int = 1,
                 start: complex | None = None,
                 end: complex | None = None) -> complex:
    """Function for generating random complex numbers"""
    return rccomplex(random.choice, realprelength, realpostlength,
                     imagprelength, imagpostlength, start, end)


def cryptocomplex(realprelength: int = 1,
                  realpostlength: int = 1,
                  imagprelength: int = 1,
                  imagpostlength: int = 1,
                  start: complex | None = None,
                  end: complex | None = None) -> complex:
    """Function for generating cryptographically safe and random
     complex numbers"""
    return rccomplex(secrets.choice, realprelength, realpostlength,
                     imagprelength, imagpostlength, start, end)


def rcstr(choice: Choice, length: int = 1) -> str:
    """Temporary function to take in a choice function"""
    if length <= 0:
        raise WrongLengthError(f'invalid length: {length}')

    return_val = ''
    for i in range(length):
        # Cut out all the spaces of string.printable
        return_val += choice(string.printable[:-6])
    return return_val


def randostr(length: int = 1) -> str:
    """Function for generating a random ascii string"""
    return rcstr(random.choice, length)


def cryptostr(length: int = 1) -> str:
    """Function for generating a cryptographically safe and random
     ascii string"""
    return rcstr(secrets.choice, length)


def rcabc(choice: Choice, length: int = 1) -> str:
    """Temporary function to take in a choice function"""
    if length <= 0:
        raise WrongLengthError(f'invalid length: {length}')

    return_val = ''
    for i in range(length):
        return_val += choice(string.ascii_letters)
    return return_val


def randoabc(length: int = 1) -> str:
    """Function for generating a random abc string"""
    return rcabc(random.choice, length)


def cryptoabc(length: int = 1) -> str:
    """Function for generating a cryptographically safe and random
     abc string"""
    return rcabc(secrets.choice, length)


def randointlen(minlen: int = 1, maxlen: int = 100) -> int:
    """Function for generating random integers with a random length"""
    return cast(int, randoint(length=random.randint(minlen, maxlen)))


def cryptointlen(minlen: int = 1, maxlen: int = 100) -> int:
    """Function for generating cryptographically safe and random
     integers with a random length"""
    return cast(int, cryptoint(length=randomizer.randint(minlen, maxlen)))


def randofloatlen(minlen: int = 1, maxlen: int = 100) -> float:
    """Function for generating random floating point numbers
     with a random length"""
    return randofloat(prelength=random.randint(minlen, maxlen),
                      postlength=random.randint(minlen, maxlen))


def cryptofloatlen(minlen: int = 1, maxlen: int = 100) -> float:
    """Function for generating cryptographically safe and random
     floating point numbers with a random length"""
    return cryptofloat(prelength=randomizer.randint(minlen, maxlen),
                       postlength=randomizer.randint(minlen, maxlen))


def randocomplexlen(minlen: int = 1, maxlen: int = 100) -> complex:
    """Function for generating random complex numbers with a random length"""
    return randocomplex(realprelength=random.randint(minlen, maxlen),
                        realpostlength=random.randint(minlen, maxlen),
                        imagprelength=random.randint(minlen, maxlen),
                        imagpostlength=random.randint(minlen, maxlen))


def cryptocomplexlen(minlen: int = 1, maxlen: int = 100) -> complex:
    """Function for gnerating cryptographically safe and random
     complex numbers with a random length"""
    return cryptocomplex(realprelength=randomizer.randint(minlen, maxlen),
                         realpostlength=randomizer.randint(minlen, maxlen),
                         imagprelength=randomizer.randint(minlen, maxlen),
                         imagpostlength=randomizer.randint(minlen, maxlen))


def randostrlen(minlen: int = 1, maxlen: int = 100) -> str:
    """Function for generating a random ascii string with a random length"""
    return randostr(length=random.randint(minlen, maxlen))


def cryptostrlen(minlen: int = 1, maxlen: int = 100) -> str:
    """Function for generating a cryptographically safe and random
     ascii string with a random length"""
    return cryptostr(length=randomizer.randint(minlen, maxlen))


def randoabclen(minlen: int = 1, maxlen: int = 100) -> str:
    """Function for generating a random abc string with a random length"""
    return randoabc(length=random.randint(minlen, maxlen))


def cryptoabclen(minlen: int = 1, maxlen: int = 100) -> str:
    """Function for generating a cryptographically safe and random
     abc string with a random length"""
    return cryptoabc(length=randomizer.randint(minlen, maxlen))


def rcfirstname(choice: Choice) -> str:
    """Temporary function to take in a choice function"""
    return choice(first_names)


def randofirstname() -> str:
    """Function for generating a random first name"""
    return rcfirstname(random.choice)


def cryptofirstname() -> str:
    """Function for generating a cryptographically safe and random
     first name"""
    return rcfirstname(secrets.choice)


def rclastname(choice: Choice) -> str:
    """Temporary function to take in a choice function"""
    return choice(last_names)


def randolastname() -> str:
    """Function for generating a random last name"""
    return rclastname(random.choice)


def cryptolastname() -> str:
    """Function for generating a cryptographically safe and random
     last name"""
    return rclastname(secrets.choice)


def randoemail(address: str = 'faker', dot_extension: str = 'com') -> str:
    """Function for generating a random email"""
    first_name = randofirstname().lower()
    last_name = randolastname().lower()
    return f'{first_name}{last_name}@{address}.{dot_extension}'


def cryptoemail(address: str = 'faker', dot_extension: str = 'com') -> str:
    """Function for generating a cryptographically safe and random email"""
    first_name = cryptofirstname().lower()
    last_name = cryptolastname().lower()
    return f'{first_name}{last_name}@{address}.{dot_extension}'


def randophone(country_code: int = 1, exchange: int = 555) -> str:
    """Function for generating a random phone number"""
    return f'+{country_code} ({randoint(3)}) {exchange}-{randoint(4)}'


def cryptophone(country_code: int = 1, exchange: int = 555) -> str:
    """Function for generating a cryptographically safe and random
     phone number"""
    return f'+{country_code} ({cryptoint(3)}) {exchange}-{cryptoint(4)}'
