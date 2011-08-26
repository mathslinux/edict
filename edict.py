#!/usr/bin/python
# encoding: utf-8
""" Emacs dictionary wrapper

Author: mathslinux <riegamaths@gmail.com>
URL: http://mathslinux.org
Version: 0.0.2

"""

__author__ = 'mathslinux'
__version__ = '0.0.2'

# Append xgoogle to system path
import sys, os
import getopt

_engine = ('google', 'stardict')

_languages = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bh': 'Bihari',
    'bg': 'Bulgarian',
    'my': 'Burmese',
    'ca': 'Catalan',
    'chr': 'Cherokee',
    'zh': 'Chinese',
    'zh-CN': 'Chinese_simplified',
    'zh-TW': 'Chinese_traditional',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'dv': 'Dhivehi',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gn': 'Guarani',
    'gu': 'Gujarati',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'id': 'Indonesian',
    'iu': 'Inuktitut',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish',
    'ky': 'Kyrgyz',
    'lo': 'Laothian',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mk': 'Macedonian',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Oriya',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt-PT': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sa': 'Sanskrit',
    'sr': 'Serbian',
    'sd': 'Sindhi',
    'si': 'Sinhalese',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tl': 'Tagalog',
    'te': 'Telugu',
    'th': 'Thai',
    'bo': 'Tibetan',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'ug': 'Uighur',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'yi': 'Yiddish'
    };

class GoogleTranslator(object):
    """ Google search engine
    """

    def __init__(self):
        pass

    def translate(self, search_text, f='', t='zh'):
        """ !!!Note, if f is empty, auto-detects the source language.
        if t is empty, the real value of lang_to is 'zh'
        
        """

        if t not in _languages:
            raise 'Translate to language %s is not supported.' % t
        if not f and f not in _languages:
            raise 'Translate from language %s is not supported' % (f)

        buf = {'v': '1.0',
               'q': 'search_text',
               'langpair': '%s|%s' %(f, t)
               }
        buf = urllib.urlencode(buf)
        translate_url = "http://ajax.googleapis.com/ajax/services/language/translate?"
        try:
            resp = urllib2.urlopen(translate_url, buf)
            data = json.loads(resp.read())
            if data['responseStatus'] != 200:
                raise "Something error happen."
            return data['responseData']['translatedText']
        except:
            raise "Something error happen."
        
        return None
        
class StardictTranslator(object):
    """ Use stardict to translate
    """

    def __init__(self):
        pass

    def translate(self, search_text):
        return 'Not support now'
        
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

def do_search(engine, search_text, f, t):
    if engine not in _engine:
        print 'Not support search engine.'

    translation = ''
    if engine == 'google':
        translation = GoogleTranslator().translate(search_text, f, t)
    elif engine == 'stardict':
        translation = StardictTranslator.translate(search_text, f, t)
    else:
        return 'No such engine %s' %(self.engine)

    if translation:
        return translation
    else:
        print 'Something error.'
                
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
    print do_search(engine, search_text, f, t)

    
