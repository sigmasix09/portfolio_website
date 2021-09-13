.. Password_Checker documentation master file, created by
    sphinx-quickstart on Tue Sep 29 13:44:03 2020.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to Password_Checker's documentation!
============================================

The password_checker module will help user to know the number of times
their password has been pwned till date so that the user can update the
password accordingly and prepare better and stronger passwords. The user
sends a HTTP requst using requests module of python without an actual
browser interaction. The API request is made from the user side which
uses 'K-anonymity' technique for the anonymized data. In this technique
the first five characters of the password hash code are sent to the API.
The `Hash_Generator <https://passwordsgenerator.net/sha1-hash-generator/>`_
which generates a value of fixed length for each input it gets eg SHA1, md5 etc.
The important thing is to encode the input in 'utf-8' before converting it to hash value.

Required Python Libraries
-------------------------

List of required python libraries::

    import hashlib
    import sys
    import traceback
    import requests

Function 1: read_pwd_file
-------------------------

The function :meth:`read_pwd_file` takes file name as the input value
for a pre-defined directory. The function :meth:`pwned_api_check`
function is called to check each password from the provided file.
:param filename: Contains dummy passwords for testing purpose.
:return: None

Example code::

    def read_pwd_file(filename) -> None:
        try:
            with open(filename, 'r') as file_handle:
                pwd_list = file_handle.read().splitlines()
                for item in pwd_list:
                    pwned_count = pwned_api_check(item)
                    if pwned_count:
                        print(f'Your password was pwned {pwned_count} times, change your password.')
                    else:
                        print('Your password has not been pwned yet, please continue using it.')
                file_handle.close()
        except BaseException:
            traceback.print_exc(file = sys.stdout)

Function 2: pwned_api_check
---------------------------

The function :meth:`pwned_api_check` reads the password from the provided
file and converts it to the hash code. The function resp_api_data is
called with first 5 hash code characters which returns the API response.
The fucntion :meth:`get_password_leaks_count` is called with return value of
:meth:`resp_api_data` function and the remaining hash code characters of the password.
:param password: password
:return: No. of times passwrod has been pwned.

Example code::

    def pwned_api_check(password) -> int:
        sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        first5_char, tail_char = sha1password[:5], sha1password[5:]
        response_value = resp_api_data(first5_char)
        password_leak_count = get_password_leaks_count(response_value, tail_char)
        return password_leak_count

Function 3: resp_api_data
-------------------------

The :meth:`resp_api_data` fucntion takes the first five characters of the
password hash code. The function requests the API with first five
hash characters returns the API response.
:param first5_char: The first five characters of the password hash code.
:return: API response

Example code::

    def resp_api_data(first5_char) -> str:
        url = f'https://api.pwnedpasswords.com/range/{first5_char}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error fetching: {response.status_code}, check and try again.')
        return response

Function 4: get_password_leaks_count
------------------------------------

The function :meth:`get_password_leaks_count` takes the API response and
the tail hash characters as inputs. The function compares the tail
has characters with the hash characters from API response value and
returns the number of times the hash code is pwned.
:param response_value: Return value of resp_api_data i.e API response
:param tail_char: The tail characters of the password hash code.
:return: no. of times the hash code is pwned.

Example code::

    def get_password_leaks_count(response_value, tail_char) -> int:
        response_value = (line.split(':') for line in response_value.text.splitlines())
        for hashes, count in response_value:
            if tail_char == hashes:
                return count

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`search`