#python requests
import requests as rq
# beautiful soup is used to parse through the HTML we get from requests
from bs4 import BeautifulSoup as bsoup
#regex
import re
import sys

url = sys.argv[1]
keyword = sys.argv[2]

# python application with input parameters "URL" and "keyword to search for"
# cron job runs application and sends daily email with results over last 24 hours

# empty list for keyword hits declared here
keywordList=[]

# crawl function
def crawlPage(url,keyword):
    baseURL = url
    # request to webpage
    r=rq.get(url)
    # use Beautifulsoup on content from request
    c = r.content
    soup = bsoup(c, features="html.parser")
    
    #look for all anchor tags
    content = soup.find_all("a")
    #regex expression for keyword
    regex = r"" + re.escape(keyword) + "s?"
    keyword_pattern = re.compile(regex, re.IGNORECASE)
    #loop through content and retrieve results according to keyword
    for a in content:
        match = keyword_pattern.findall(a.text)
        if match != []:
            #append results to keyword list    
            keywordList.append(a.text+":")
            keywordList.append(a['href'])        
        
    # append href from "next" button to URL for next request
    try:
        nextPage = soup.find("a",attrs = {'class': 'button next'})
        newURLregex = r"" + re.escape("/search/") + r"(.*)"
        newURL = re.sub(newURLregex, nextPage['href'], baseURL)
        # recursive call to top of the function
        crawlPage(newURL, keyword)
    except:
        # nextPage['href'] will return 'NoneType" when craigslist hits end of
        # results for the category, so exit at this point
        print("End of results")
        return

#execute crawl    
crawlPage(url,keyword)

#write output to a file
with open('crawlResults.txt', 'w') as filehandle:  
    for listitem in keywordList:
        filehandle.write('%s\n' % listitem)