#!/usr/bin/python
# encoding: utf-8
""" Emacs dictionary wrapper

Author: mathslinux <riegamaths@gmail.com>
URL: http://mathslinux.org
Version: 0.0.1

For google engine i use the xgoogle's Translator module to get it work. 
chinese this version.
"""

__author__ = 'mathslinux'
__version__ = '0.0.1'

# Append xgoogle to system path
import sys, os
sys.path.append(os.path.join(os.path.split(__file__)[0], 'xgoogle'))

import getopt

from xgoogle.translate import Translator, TranslationError

class Google(object):
    """ Google search engine
    
    Use the xgoogle to translate.
    """

    def __init__(self):
        pass

    def translate(self, search_text, f='', t='zh'):
        """ !!!Note, if f is empty, auto-detects the language.
        if t is empty, the real value of lang_to is 'en'
        """
        try:
            return Translator().translate(search_text, lang_from=f, lang_to=t).encode('utf-8')
        except TranslationError, e:
            return e

class Stardict(object):
    """ Use stardict to translate
    """

    def __init__(self):
        pass

    def translate(self, search_text):
        return 'Not support now'

class Edict(object):
    def __init__(self, engine='google'):
        self.engine = engine
        
    def translate(self, search_text, f='', t='zh'):
        if self.engine == 'google':
            return Google().translate(search_text, f, t)
        elif self.engine == 'stardict':
            return Stardict.translate(search_text, f, t)
        else:
            return 'No such engine %s' %(self.engine)
        
def usage():
    usage = """Usage: edict [options] text
       -h, --help
          help
       -v, --version
           output version and exit
       -e, --engine
           search engine. eg. google
       -f, --from
           from language
       -t, --to
           to language"""
    print usage
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
	sys.exit()

    engine = 'google'
    f = ''
    t = 'en'
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hve:f:t:", ["help", "version", "engine=", "from=", "to="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-v", "--version"):
            print 'edict %s' %(__version__)
            sys.exit()
        elif o in ("-e", "--engine"):
            engine = a
        elif o in ("-f", "--from"):
            f = a
        elif o in ("-t", "--to"):
            t = a
        else:
            assert False, "invalid option %s" %(o)
            
    search_text = ' '.join(args).strip()
    print search_text
    print Edict(engine).translate(search_text, f, t)

