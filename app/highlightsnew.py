#! python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pdb
import urllib
import errno




#debugging
#import pdb #use pdb.set_trace() to break


def processDOI(myDOIs):

    global imgurls
    global articlelink
    global articletitles
    global authorslist
    global results

    '''

    dealing with creating custom URLS for each DOI

    '''
    #Steps to prepare....

    #get current YYYYMMDD
    import datetime
    date = datetime.date.today()
    datecode = datetime.datetime.now().strftime("%Y%m%d")
    



    #dictionary to match stripped dois with their corresponding coden (for URL formation)
    coden_match = { 
        'ar': 'achre4',
        'jf': 'jafcau',
        'ac': 'ancham',
        'am': 'aamick',
        'bi': 'bichaw',
        'bc': 'bcches',
        'bm': 'bomaf6',
        'ab': 'abseba',
        'cs': 'accacs',
        'oc': 'acscii',
        'cb': 'acbcct',
        'ed': 'jceda8',
        'je': 'jceaax',
        'ci': 'jcisd8',
        'cn': 'acncdm',
        'tx': 'crtoec',
        'cr': 'chreay',
        'ct': 'jctcce',
        'cm': 'cmatex',
        'co': 'acsccc',
        'cg': 'cgdefu',
        'ef': 'enfuem',
        'es': 'esthag',
        'ez': 'esthag',
        'ie': 'iecred',
        'id': 'aidcbc',
        'ic': 'inocaj',
        'ja': 'jacsat',
        'la': 'langd5',
        'mz': 'amlccd',
        'ma': 'mamobx',
        'jm': 'jmcmar',
        'ml': 'amclct',
        'mp': 'mpohbp',
        'nn': 'ancac3',
        'nl': 'nalefd',
        'np': 'jnprdf',
        'jo': 'joceah',
        'ol': 'orlef7',
        'op': 'oprdfk',
        'om': 'orgnd7',
        'ph': 'apchd5',
        'jp': 'jpcafh',
        'jpb': 'jpcbfk',
        'jpc': 'jpccck',
        'jz': 'jpclcd',
        'pr': 'jprobs',
        'se': 'ascefj',
        'sc': 'ascecg',
        'sb': 'asbcd6',
        'acsaccounts': 'achre4',
        'acsjafc': 'jafcau',
        'acsanalchem': 'ancham',
        'acsami': 'aamick',
        'acsbiochem': 'bichaw',
        'acsbioconjchem': 'bcches',
        'acsbiomac': 'bomaf6',
        'acscatal': 'accacs',
        'acscentsci': 'acscii',
        'acschembio': 'acbcct',
        'acsjchemed': 'jceda8',
        'acsjced': 'jceaax',
        'acsjcim': 'jcisd8',
        'acschemneuro': 'acncdm',
        'acschemrestox': 'crtoec',
        'acschemrev': 'chreay',
        'acsjctc': 'jctcce',
        'acschemmater': 'cmatex',
        'acscombsci': 'acsccc',
        'acscgd': 'cgdefu',
        'acsenergyfuels': 'enfuem',
        'acsest': 'esthag',
        'acsestlett': 'estlcu',
        'acsacsiecr': 'iecred',
        'acsinfecdis': 'aidcbc',
        'acsinorgchem': 'inocaj',
        'jacs': 'jacsat',
        'acslangmuir': 'langd5',
        'acsmacrolett': 'amlccd',
        'acsmacromol': 'mamobx',
        'acsjmedchem': 'jmcmar',
        'acsmedchemlett': 'amclct',
        'acsmolpharmaceut': 'mpohbp',
        'acsnano': 'ancac3',
        'acsnanolett': 'nalefd',
        'acsjnatprod': 'jnprdf',
        'acsjoc': 'joceah',
        'acsorglett': 'orlef7',
        'acsoprd': 'oprdfk',
        'acsorganomet': 'orgnd7',
        'acsomega': 'acsodf',
        'acsphotonics': 'apchd5',
        'acsjpca': 'jpcafh',
        'acsjpcb': 'jpcbfk',
        'acsjpcc': 'jpccck',
        'acsjpclett': 'jpclcd',
        'acsjproteome': 'jprobs',
        'acssensors': 'ascefj',
        'acssuschemeng': 'ascecg',
        'acssynbio': 'asbcd6'
    }


    # create list of urls with stripped dois, and list of stripped dois 
    clean_journal = []

    for y in myDOIs:
        y = y.strip()
        y = y.replace("10.1021/","").replace(".","")
        clean_journal.append(y)

    #Cross-check stripped doi with journal coden dictionary, and use the coden.
        #remove journal IDs from clean_journal to keep just the cleaned journal name

    journal_name = []

    for d in clean_journal:
        d = d[:-7]
        journal_name.append(d)

    
    # convert list of shortened journal names into new list of corresponding codens
    converted_journal = []
    for n in journal_name:
        coden = coden_match[n]
        converted_journal.append(coden)


    



    AUTHOR_XPATH = ("//span[@class=\"hlFld-ContribAuthor\"]/span[@class=\"hlFld-ContribAuthor\"]/a | " + 
    "//*[@id=\"authors\"]/span/span/span/x | //*[@id=\"authors\"]/span/span/a[@href='#cor1'] | //*[@id=\"authors\"]/span/span/a[@href='#cor2'] | //*[@id=\"authors\"]/span/span/a[@href='#cor3']")
        
    
    '''
    Loop through the DOIS to find information from each article page. add that info to lists. 

    '''



    #instantiate the lists that the process will populate
        
    articletitles = []
    href_list = [] 
    articlelink = []
    authorslist = []


    driver = webdriver.PhantomJS(service_log_path='/home/deploy/pubshelper/app/ghostdriver.log', cd executable_path="/usr/local/bin/phantomjs")
    driver.set_window_size(1120,550)

    for i in myDOIs:

        #go to full article page by adding URL prefix to DOI

        driver.get("http://pubs.acs.org/doi/full/" + i)

        #wait ten seconds and get title text
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))


        # add title to list of titles (with special characters)
        articletitles.append(title.get_attribute('innerHTML'))
        
        # create article URLS for PB, add to list
        articlelink.append("/doi/abs/" + str(i) + "\n")

        # get authors
        authors = driver.find_elements_by_xpath(AUTHOR_XPATH)

        #join the text in the array of the correctly encoded authors
        authors_scrape = []
        for author in authors:
            authors_scrape.append(author.text)
            
        if len(authors_scrape) > 2:
            if authors_scrape[1] == 'and':
                authors_scrape[1] = ' and '
                authorsjoined = (''.join(authors_scrape))
            elif authors_scrape[2] == 'and':
                authors_scrape[2] = ' and '
                authorsjoined = (''.join(authors_scrape))
            else: 
                authorsjoined = (''.join(authors_scrape))
                authorsjoined = authorsjoined.replace(',', ', ').replace(' and', 'and ')
        else: 
            authorsjoined = (''.join(authors_scrape))
        
        authorslist.append(authorsjoined)



        
        #click figures link
        driver.find_element_by_class_name('showFiguresLink').click()

        img_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
        toc_href = img_box.find_element_by_css_selector('a').get_attribute('href')

        # add toc_href to list of URLS to download later and rename according to the DOI
        href_list.append(toc_href)
        
     

        # open a new tab and repeat
        driver.implicitly_wait(8) # seconds
        driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')


    driver.close()
    driver.quit()
    
    # #form img prefix according to checked coden [for image hosted on PB]
    # cleanhref = []
    # for href in href_list:
    #     href = href.split("/large/", 1)[1]
    #     cleanhref.append(href)

    # imgurls = []
    # for coden, href in zip(converted_journal, cleanhref):
    #     img_prefix = "/pb-assets/images/" + str(coden) + "/highlights/" + str(datecode) + "/" + str(href)
    #     imgurls.append(img_prefix)

    #form img prefix according to checked coden
    imgurls = []
    img_filenames = []
    for coden, journal in zip(converted_journal, clean_journal):
        img_prefix = ("/pb-assets/images/" + str(coden) + "/highlights/" + str(datecode) + 
        "/" + str(journal) + ".jpeg")
        img_filename = str(journal + ".jpeg")
        img_filenames.append(img_filename)
        imgurls.append(img_prefix)
    

    


    '''
    download mp3s from list of image href

    '''

    urlfilenamepair = zip(href_list, clean_journal)
    for href, y in urlfilenamepair:
            filename =  y + ".jpeg"
            urllib.urlretrieve(href, filename)


    #combine results lists into one list

    
    results = zip(articlelink, imgurls, articletitles, authorslist, href_list, img_filenames)
    
    return results




   




   










