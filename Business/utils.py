import os
import sys
try:
    import requests
except ModuleNotFoundError:
    if (str(input("Module requests missing. Install [Y,n]?")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install requests')
    import requests
try:
    import urllib
except ModuleNotFoundError:
    if (str(input("Module urllib missing. Install [Y,n]?")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install urllib')
    import urllib
try:
    import pandas as pd
except ModuleNotFoundError:
    if (str(input("Module pandas missing. Install [Y,n]?")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install pandas')
    import pandas as pd
try:
    from requests_html import HTML
    from requests_html import HTMLSession
except ModuleNotFoundError:
    if (str(input("Module requests_html missing. Install [Y,n]?")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install requests_html')
    from requests_html import HTML
    from requests_html import HTMLSession

def get_page_source(url):
    htmlSession = HTMLSession()
    response = htmlSession.get(url)
    return response

def search_google(query):
    parsed = urllib.parse.quote_plus(query)
    response = get_page_source("https://www.google.com/search?q={0}".format(parsed))
    pageLinks = list(response.html.absolute_links)
    domainsToRemove = ("https://www.google.", 
                      "https://google.", 
                      "https://webcache.googleusercontent.", 
                      "http://webcache.googleusercontent.", 
                      "https://policies.google.",
                      "https://support.google.",
                      "https://maps.google.")
    for url in pageLinks[:]:
        if url.startswith(domainsToRemove):
            pageLinks.remove(url)
    return pageLinks
def get_tld(url):
    return url.split("/")[0]