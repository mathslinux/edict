#!/usr/bin/python
# encoding: utf-8
""" Emacs dictionary wrapper

Author: mathslinux <riegamaths@gmail.com>
URL: http://mathslinux.org
Version: 0.0.2

"""

__author__ = 'mathslinux'
__version__ = '0.0.2'
# git test
import sys, os
import getopt
import urllib, urllib2
import re
from struct import unpack

try:
    import simplejson as json
except:
    raise ImportError, 'Cant find simplejson, please install it.'

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

class TranslationError(Exception):
    pass

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
            raise TranslationError, 'Translate to language %s is not supported.' % t
        if f and f not in _languages:
            raise TranslationError, 'Translate from language %s is not supported' % f

        buf = {'v': '1.0',
               'q': '%s' % search_text,
               'langpair': '%s|%s' %(f, t)
               }
        buf = urllib.urlencode(buf)
        translate_url = "http://ajax.googleapis.com/ajax/services/language/translate?"
        try:
            resp = urllib2.urlopen(translate_url, buf)
            data = json.loads(resp.read())
            if data['responseStatus'] != 200:
                raise TranslationError, "Response error."
            return data['responseData']['translatedText']
        except:
            raise TranslationError, "Something error happen."
        
        return None


class StardictIdx(object):
    """ Parse the dictionary of stardict format
    
    the format is stored in .idx file, which looks like:
    |word|offset|length|
    word: terminated by '\0'.
    offset: translation's offset in .dict file
    length: translation's length in .dict file
    
    """

    def __init__(self, idx_file):
        self.idx = self._get_dict_idx(idx_file)
        

    def _get_dict_idx(self, idx_file):
        """ Parse the .idx file
        
        the .idx file will be parse to dict idx:
        {
        word1: (offset1, length1),
        word2: (offset2, length2),
        ... ...
        wordn: (offsetn, lengthn)
        }
        """

        idx = {}
        idx_buf = open(idx_file, 'rb').read()
        pattern = r'(.+?\x00.{8})'
        for record in re.findall(pattern, idx_buf):
            c = record.find('\x00')
            word = record[0:c]
            offset, length = unpack('!II', record[-8:])
            idx[word] = (offset, length)
        return idx

    def __getitem__(self, word):
        for i in self.idx.keys():
            if cmp(word.upper(), i.upper()) == 0:
                return self.idx[i]
        
    
class StardictTranslator(object):
    """ Translation from stardict dictionary
    """
    
    def __init__(self, idx_file, dict_file):
        self.dict_file = dict_file
        self.idx = StardictIdx(idx_file)

    def _get_translation(self, word):

        try:
            offset, length = self.idx[word]
        except TypeError:
            raise TranslationError

        _dict_file = open(self.dict_file, 'r')
        _dict_file.seek(offset)
        buf = _dict_file.read(length)
        _dict_file.close()

        return buf

    def translate(self, search_text, f='', t='zh'):
        """ Do the translating
        """

        if (f and f != 'en') or t != 'zh':
            raise TranslationError

        return self._get_translation(search_text)
            
    

class ICIBATranslator(object):
    """ Use iciba api to translate
    """

    def __init__(self):
        """
        """
        pass

    def translate(self):
        """
        """

        return None
        
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


_current_path = os.path.split(__file__)[0]
_idx_file = os.path.join(_current_path, 'stardict-oxford-gb-2.4.2/oxford-gb.idx')
_dict_file = os.path.join(_current_path, 'stardict-oxford-gb-2.4.2/oxford-gb.dict')
def do_search(engine, search_text, f, t):
    if engine not in _engine:
        print 'Not support search engine.'

    translation = ''

    try:
        if engine == 'google':
            translation = GoogleTranslator().translate(search_text, f, t)
            translation = translation.encode('utf-8')
        elif engine == 'stardict':
            translation = StardictTranslator(_idx_file, _dict_file).translate(search_text, f, t)
        else:
            return 'No such engine %s' %(self.engine)

        print search_text
        print translation

    except TranslationError:
        print search_text
        print '!!!translate error.'
                
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
	sys.exit()

    engine = 'stardict'
    f = ''
    t = 'zh'
    
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
    do_search(engine, search_text, f, t)

    
