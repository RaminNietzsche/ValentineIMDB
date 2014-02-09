#-*- coding: utf-8 -*-
import config

class normalize(object):

    """
    return simple normalized text
    """

    def __init__(self, string):
        """
        """
        if isinstance(string, unicode):
            self.string = string.strip()
        else:
            self.string = str(string).strip()
        self.string = self.string.lower()

    def remove_bad_char(self):
        """
        remove all bad cahr-braket-words
        """
        find_bad = len(self.string)
        for rule in config.bad_char:  
            self.string = self.string.replace(rule, ' ')
        for rule in config.brackets:
            self.string = self.string.replace(rule, '')
        for rule in config.reject_words:
            tmp = self.string.find(rule.lower())
            if tmp < find_bad and tmp > 0:
                find_bad = tmp
            # print find_bad
        self.string = ''.join(self.string[:find_bad])
            
            #self.string = self.string.replace(rule.lower(), '')

    def _rstrip(self):
        self.string = self.string.rstrip()

    def remove_type(self):
        """
        remove all bad cahr-braket-words
        """
        self.string = " ".join(self.string.split('.')[:-1])

def simple_normalize(string):
    """
    for base search use this
    """
    if not string:
        return
    new_string = normalize(string)
    new_string.remove_type()
    new_string.remove_bad_char()
    new_string._rstrip()
    return new_string.string
