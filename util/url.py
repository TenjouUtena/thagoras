import re

urlre = '(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.\&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F\&\#]))+)'
#urlre = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?]))'


## Get a image URL from a URL that may not be an image
def urlImageGetter(url):
    hostfind = re.compile(r'[a-z0-9.\-]+[.][a-z]{2,4}/')
    imageendings = ['png','gif','jpg','bmp']

    ##If we end in a image ending, then we're probably already an image url
    if(url[-3:] in imageendings):
        return url

    hostmatch = hostfind.search(url)
    host = ""
    if(hostmatch):
        host = hostmatch.group(0)[:-1]

    ## First if it is imgur, just append .png on the end, imgur will send something sane back
    if(('imgur' in host) and (not url[-3:] in imageendings)):
        return url+'.png'


    ## Just return the URL back if we don't find anything
    return url



