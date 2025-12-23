from checker.checker import checker
from scraper.scraper import scrape

def start():
    option = input("""Proxy Checker/Scraper -
                   
[1] Scrape Proxies
[2] Check Proxies
[3] Export Valid Proxies
[4] Exit

Choose An Option >> """)
    
    print()
    
    if option == '1':
        print('Starting Scrape!\n')
        scrape()
    elif option == '2':
        url = input('What site would you like to check the proxies againt (https://example.com) >> ')
        success_key = input('What shows a valid request (<title>example</title>) >> ')
        threads = input('How many threads >> ')
        
        print()

        checker(url, success_key, int(threads), int(threads))
    elif option == '4':
        exit('Exiting!')
    
start()