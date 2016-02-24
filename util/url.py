# -*- coding: utf-8 -*-

import re
import bs4, urllib2

urlre = '(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.\&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F\&\#]))+)'


## Get a image URL from a URL that may not be an image
def urlImageGetter(url):
    hostfind = re.compile(r'[a-z0-9.\-]+[.][a-z]{2,4}/')
    imageendings = ['png','gif','jpg','bmp']

    ## ask it if it will return an image:
    res = urllib2.urlopen(url)
    if(res.info().gettype().lower().startswith('image')):
        return url

    ##If we end in a image ending, then we're probably already an image url
    if(url[-3:] in imageendings):
        return url

    hostmatch = hostfind.search(url)
    host = ""
    if(hostmatch):
        host = hostmatch.group(0)[:-1]

    ## First if it is imgur, just append .png on the end, imgur will send something sane back
    ## This doesn't work for albums. ☹
    if(('imgur' in host) and (not url[-3:] in imageendings)):
        return url+'.png'

    ## at this point we need to find the image in the HTML page
    soup = bs4.BeautifulSoup(res.read(), "html.parser")

    ## This would at least for various boorus
    img = soup.find_all('img',id='image')
    if(img):
        return(img[0]['src'])
    ## Some booru doesn't reutn full url for pic on this method

    ##Sankaku seems to 403 us for beign a robbit.

    ## Just return the URL back if we don't find anything
    return url



