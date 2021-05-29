"""
A modified python3-mechanicalsoup for local usage
The new name is mechanicalsoup to avoid import conflic
Modifier: Nong Hoang Tu <dmknght@parrotsec.org>

Original source: https://github.com/MechanicalSoup/MechanicalSoup
Original version: 1.0.0
License:

The MIT License (MIT)

Copyright (c) 2014

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class LinkNotFoundError(Exception):
    """Exception raised when mechanicalsoup fails to find something.

    This happens in situations like (non-exhaustive list):

    * :func:`~mechanicalsoup.StatefulBrowser.find_link` is called, but
      no link is found.

    * The browser was configured with raise_on_404=True and a 404
      error is triggered while browsing.

    * The user tried to fill-in a field which doesn't exist in a form
      (e.g. browser["name"] = "val" with browser being a
      StatefulBrowser).
    """
    pass
