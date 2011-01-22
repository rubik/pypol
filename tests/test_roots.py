#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

'''
pypol - a Python library to manipulate polynomials and algebraic fractions.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Requirements:
- Python 2.6 (or 2.7)
'''

import pypol.roots as roots

class TestRoots(object):
    def setUp(self):
        pass

    def testRuffini(self):
        pass

    def testQuadratic(self):
        pass

    def testCubic(self):
        pass

    def testNewton(self):
        pass

    def testHalley(self):
        pass

    def testHouseholder(self):
        pass

    def testSchroeder(self):
        pass

    def testLaguerre(self):
        pass

    def testBrent(self):
        pass

    def testDurandKerner(self):
        pass

if __name__ == '__main__':
    import sys
    import os.path
    py.test.main(args=[os.path.abspath(__file__)] + sys.argv[1:])