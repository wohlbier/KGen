#!/usr/bin/python
#
# compflag.py: generates include INI file from CESM build log
#
# Version: 0.1
# Author : Youngsung Kim ( kgen@ucra.edu )

import os
import sys
import optparse
from collections import OrderedDict
from kgen_utils import strip_quote

# Python version check
if sys.hexversion < 0x020700F0:
    print 'ERROR: KGEN works with Python Version 2.7 or later.'
    sys.exit(-1)


class CompFlagConfig(object):
    def __init__(self, argv=None):

        self.attrs = OrderedDict()

        self.attrs['compflag'] = OrderedDict()
        self.attrs['compflag']['version'] = [ 0, 1, '0' ]

        self.attrs['strace'] = 'strace.log'

        self.attrs['build'] = OrderedDict()
        self.attrs['build']['clean'] = ''
        self.attrs['build']['cmdline'] = ''
        self.attrs['build']['cwd'] = '.'

        self.attrs['ini'] = 'include.ini'

        self.attrs['rebuild'] = OrderedDict()

        self.attrs['prerun'] = OrderedDict()
        self.attrs['prerun']['clean'] = ''
        self.attrs['prerun']['build'] = ''

        self.attrs['macro'] = OrderedDict()

        self.attrs['include'] = OrderedDict()

        self.attrs['object'] = OrderedDict()

        self.attrs['debug'] = OrderedDict()

        parser = optparse.OptionParser(version='COMPFLAG version %d.%d.%s'%tuple(self.attrs['compflag']['version']))

        parser.add_option("-s", "--strace", dest="strace", action='store', type='string', default=None, help="strace options")
        parser.add_option("-b", "--build", dest="build", action='append', type='string', default=None, help="build options")
        parser.add_option("-i", "--include-ini", dest="include_ini", action='store', type='string', default=None, help="INI options")
        parser.add_option("-D", dest="macro", action='append', type='string', default=None, help="Define macros in INI file")
        parser.add_option("-I", dest="include", action='append', type='string', default=None, help="Add include paths in INI file")
        parser.add_option("-J", dest="object", action='append', type='string', default=None, help="Add object paths in INI file")
        parser.add_option("--rebuild",  dest="rebuild", action='append', type='string', default=None, help="List of reusable files")
        parser.add_option("--prerun",  dest="prerun", action='append', type='string', default=None, help="List of prerun commands")
        parser.add_option("--debug",  dest="debug", action='append', type='string', default=None, help=optparse.SUPPRESS_HELP)

        opts, args = parser.parse_args(args=argv)
#        
#        if len(args)<1:
#            print 'ERROR: At least one argument is required.'
#            sys.exit(-1)
#
        if len(args)>0:
            self.attrs['build']['cmdline'] = args[0]

        if opts.strace:
            self._save_opt(opts.strace, self.attrs['strace'])

        if opts.strace:
            self.attrs['strace'] = opts.strace

        if opts.build:
            self._save_opt(opts.build, self.attrs['build'])

        if opts.include_ini:
            self.attrs['ini'] = opts.include_ini

        if opts.macro:
            self._save_opt(opts.macro, self.attrs['macro'], append=True)

        if opts.include:
            self._save_opt(opts.include, self.attrs['include'], append=True)

        if opts.object:
            self._save_opt(opts.object, self.attrs['object'], append=True)

        if opts.rebuild:
            self._save_opt(opts.rebuild, self.attrs['rebuild'], append=True)

        if opts.prerun:
            self._save_opt(opts.prerun, self.attrs['prerun'])

        if opts.debug:
            self._save_opt(opts.debug, self.attrs['debug'], append=True)

    def _save_opt(self, opt, attr, append=False):
        if isinstance(opt, str):
            opt = [ opt ]

        if isinstance(opt, ( list, tuple ) ):
            for o in opt:
                if isinstance(o, str):
                    subopts = o.split(',')
                    for subopt in subopts:
                        if subopt:
                            if subopt.find('=')>0:
                                key, value = subopt.split('=', 1)
                                if append:
                                    if attr.has_key(key):
                                        attr[key].append(strip_quote(value))
                                    else:
                                        attr[key] = [ strip_quote(value) ]
                                else:
                                    attr[key] = strip_quote(value)
                            else:
                                if append:
                                    if attr.has_key(subopt):
                                        attr[subopt].append(True)
                                    else:
                                        attr[subopt] = [ True ]
                                else:
                                    attr[subopt] = True
                else:
                    print 'UNKNOWN TYPE: %s'%o.__class__
                    sys.exit(-1)
        else:
            print 'UNKNOWN TYPE: %s'%opt.__class__
            sys.exit(-1)

    def __getattr__(self, name):
        return self.attrs[name]
