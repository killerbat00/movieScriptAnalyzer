#!/usr/bin/python2.6
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser
import urllib2, sys, os

class MovieScript(object):
    def __init__(self, title, url, debug=False):
        self.title = title
        self.url = url
        self.filename = None
        self.script = None
        self._debug = debug

    def __str__(self):
        return ', '.join([self.title, self.url])

    '''Formats Url to point to actual script url
       url is of the form:
           www.imsdb.com/scripts/Movie-Title.html'''
    def formatUrl(self):
        root = 'http://www.imsdb.com/scripts'
        if self._debug:
            print 'Formatting url for %s into proper form...' % self.title
        #insert hypens into url
        urls = str(self.url[14:-12]).split(' ')
        #colons aren't used in urls
        for url in urls:
            if url[-1] == ':':
                url = url[:-1]
        self.url = root + '-'.join(urls) + '.html'

    def getScriptText(self):
        if self._debug:
            print 'Getting script text for %s...' % self.title

        try:
            print 'trying...'
            sFile = urllib2.urlopen(self.url)
        except urllib2.URLError as e:
            if self._debug:
                print 'Error opening %s...' % self.url
                print 'URLERROR({0}): {1}'.format(e.errno, e.strerror)
        sHtml = sFile.read()
        sSoup = BeautifulSoup(sHtml)
        self._findScriptText(sSoup)
        self._fmtFilename()

    def _findScriptText(self, soup):
        if self._debug:
            print 'Finding Script text for %s...' % self.title
        # Is under 0, 1 or 2 <pre> tags (I think)
        self.script = ''.join(soup.findAll("td", {"class" : "scrtext"}, text=True))

    def _fmtFilename(self):
        if self._debug:
            print 'Formatting filename for %s..' % self.title
        self.filename = ''.join(self.title.split(' ')) + '.txt'

    def writeFile(self):
        if not os.path.isdir(os.path.join(os.getcwd(), 'scripts')):
            if self._debug:
                print 'Creating scripts directory...'
            os.mkdir(os.path.join(os.getcwd(), 'scripts'))

        if self._debug:
            print 'Writing script to file for %s...' % self.title
        fp = open(os.path.join('scripts', self.filename), 'w')
        if not self.script==None:
            fp.write(self.script)
        fp.close()

class ScriptParse(object):
    def __init__(self, options):
        self._options = options
        if self._options.verbose:
            self._options.verbose = True

    def run(self):
        self._run()

    def _run(self):
        mainPage = "http://www.imsdb.com/all%20scripts/"
        if self._options.verbose:
            print 'Opening %s...' % mainPage
        try:
            mpFile = urllib2.urlopen(mainPage)
        except urllib2.URLError as e:
            if self._options.verbose:
                print 'Error opening %s...' % mainPage
                print 'URLError({0}): {1}'.format(e.errno, e.strerror)
            sys.exit(1)

        mpHtml = mpFile.read()
        mpSoup = BeautifulSoup(mpHtml)

        moviePs = self._getMovieListNodes(mpSoup)
        scriptList = self._convertTags(moviePs)

        for script in scriptList:
            #Edge Case
            if script.title == '8 Mile':
                continue
            script.formatUrl()
            script.getScriptText()
            script.writeFile()

        if self._options.verbose:
            print 'Done!'

    '''Get list of nodes containing movie url and Title
       @param BeautifulSoup soup
       returns list of paragraph nodes'''
    def _getMovieListNodes(self, bSoup):
        if self._options.verbose:
            print 'Retrieving nodelist of all movies...'

        # 2nd table on page, list starts at 3rd row
        tableTag = bSoup.findAll('table')[1:2]
        for t in tableTag:
            tgs = t.findAll('td')[2:]
        # extract paragraphs
        for x in tgs:
            ps = x.findAll('p')
        return ps

    '''Converts list of paragraph tags to MovieScript object
       @param list of paragraph
       returns list of MovieScripts'''
    def _convertTags(self, ps):
        if self._options.verbose:
            print 'Converting paragraph tags to movie objects...'

        # extract all link tags
        alist = []
        scripts = []
        for p in ps:
            alist.append(p.findAll('a'))

        for a in alist:
            scripts.append(MovieScript(str(a[0].get('title'))[:-7], str(a[0].get('href')), self._options.verbose))
        return scripts

def _parse_args():
    parser = OptionParser(usage='%prog [options]',
                          version='%prog 1.0',
                          description='Scrape all movie scripts available on imsdb.com and save them to file')
    parser.add_option('-v', dest='verbose', action='store_true', default=False, help='Enable verbose output')
    (options, args) = parser.parse_args()
    return options

def main():
    options = _parse_args()
    scripts = ScriptParse(options)
    scripts.run()

if __name__=='__main__':
    main()
