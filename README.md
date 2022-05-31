# Randopy
A module with random functions.
You can generate random and cryptographically safe integers, floating point numbers, complex numbers, strings, alphabet strings, emails, phone numbers,
first names, and last names.
The functions are called:
- randoint
- randofloat
- randocomplex
- randostr
- randoabc
- randoemail
- randophone
- randofirstname
- randolastname
<br /><br />Randoint's signature is `randoint(length=1, start=None, end=None, *, check_zero=True, as_str=False)`. If you want to know why the last two
exist, consider them as implementation details. The randofloat signature is `randofloat(prelength=1, postlength=1, start=None, end=None)` where "pre"length
and "post"length mean before and after the decimal. The randocomplex signature is `randocomplex(realprelength=1, realpostlength=1, imagprelength=1,
imagpostlength=1, start=None, end=None)` which is self-explanatory. The randostr signature is `randostr(length=1)`. The randoabc signature is
`randoabc(length=1)`. Randoemail's signature is `randoemail(address='faker', dot_extension='com')` where address means what comes after the @ symbol in an
email address, and the dot-extension means what comes after the "." in an email address (e.g. the default can generate: 'edwinenglish@faker.com').
Randophone's signature is `randophone(country_code=1, exchange=555)` where country-code is what comes before the "(" of a phone number, and the exchange
is the middle part of a phone number (e.g. the default can generate '+1 (488) 555-8269'). Randofirstname and randolastname take no arguments.
<br /><br />The corresponding cryptographically safe functions start with "crypto" instead of "rando" (e.g. cryptoint).
<br /><br />Additionally, there are functions that generate random stuff with a random length as well. The functions are called:
- randointlen
- cryptointlen
- randofloatlen
- cryptofloatlen
- randocomplexlen
- cryptocomplexlen
- randostrlen
- cryptostrlen
- randoabclen
- cryptoabclen
<br /><br />All of the signatures are the same (e.g. randointlen(minlen=1, maxlen=100)).
<br /><br /><br />
#### THE END
