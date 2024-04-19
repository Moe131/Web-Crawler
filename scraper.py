import re
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup


def scraper(url, resp):
    links = extract_next_links(url, resp)
    # wordFrequencies = find_word_frquency(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    scrapedLinks = list()

    # if resp.status is not 200 return 
    if resp.status != 200:
        return list()

    scrapedLinks = list()    
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        
    # finding all the <a> elements (links) in the HTML file (Note: loops and traps are not handled)
    for linkElement in soup.find_all("a"): 
        if linkElement and linkElement.get("href"):
            linkURL = linkElement.get("href")
            if linkURL.startswith("https://") or linkURL.startswith("http://") or linkURL.startswith("/"): # do not add if its not a link
                if linkURL == "/" :
                    continue
                elif linkURL.startswith("//") : # (2 slashes)  replaces url from the hostname onward
                    linkURL = f"https:{linkURL}"
                elif linkURL.startswith("/") : # (1 slash)  add path to the base URL.
                    linkURL = f"{url}{linkURL}"
                scrapedLinks.append(linkURL)

    return scrapedLinks 


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not isScrapable(url) :
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


def find_word_frquency(url, resp) ->  dict :
    """ Reads the content of a URL and returns a dictionary
        with words and their frequencies in that page """
    
     # if resp.status is not 200 return 
    if resp.status != 200:
        return dict()
    
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")
    # finding all the elements in the HTML file and getting their texts
    listOfWords = tokenize(soup.get_text())
    return computeWordFrequencies(listOfWords)


def isScrapable(url):
    """ This method checks the /robots.txt of a url and returns True if
        we are allowed to scrape it and False otherwise"""
    try:
        hostPath = removePath(url)
        rbParser = RobotFileParser()
        rbParser.set_url(hostPath+"/robots.txt")
        rbParser.read()
        return rbParser.can_fetch("*", url)
    except Exception as e:
        return False


def removePath(url):
    """ This method keep the host name of the domain and reomves
      all the remaining path"""
    parsedURL = urlparse(url)
    return f"{parsedURL.scheme}://{parsedURL.netloc}"