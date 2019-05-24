# (c) 2019 - Benedek Racz
#
# This file is part of Yard
#
# Yard is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yard is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Yard.
# If not, see <http://www.gnu.org/licenses/>.


"""
This module contains decorator functions used during render.
"""

import textwrap
import os

def fmt_comment(cmt, linelength=80, cmtChar='-- ', linesep=None):
    """
    Format comments
    """
    if linesep is None:
        linesep = os.linesep
    ret = ''
    wrapper = textwrap.TextWrapper(width=linelength-len(cmtChar))
    ret = [cmtChar + x for x in wrapper.wrap(text=cmt)]
    ret = linesep.join(ret)
    return ret


def fmt_list(strings, linelength=80, linesep=None):
    """
    Format a list. Used at sensitivitivy list of VHDL-93. Returns a comma separated string strings list.
    
    Keyword arguments:
    strings -- the list of the variables that should be joined by the comma
    """
    if linesep is None:
        linesep = os.linesep
    ret = ', '.join(strings)
    wrapper = textwrap.TextWrapper(width=linelength)
    ret = [x for x in wrapper.wrap(text=ret)]
    return linesep.join(ret)

        
def decorateVHDLHex(num):
    """ returns a hexadecimal number formatted in VHDL
    """
    return '16#{:04x}#'.format(num)


def decorate(var):
    """ decorate a variable.
    Now it is uses prefixes based on if the variable is a port or a registered signal or etc.
    And uses postfixes depending on the functionality of the variable.
    """
    functionPostfixes = {'register': '', 'readEvent': '_r_e', 'writeEnable': '_w_e',}
    decoratedName = var['name'] + functionPostfixes[var['function']]
    if var['signalClass'] == 'port':
        dirPrefixes = {'in': 'i_', 'out': 'o_',}
        var['decoratedName'] = dirPrefixes[var['dir']] + decoratedName
        return var
    if var['signalClass'] == 'signal':
        functionPrefixes = {'reg': 'q_', 'wire': 'w_', 'combinational': 'c_'}
        var['decoratedName'] = functionPrefixes[var['driverType']] + decoratedName
        return var
    raise Exception('decorate(): Unknown signalType')
    