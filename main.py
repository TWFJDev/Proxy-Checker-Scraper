from checker.checker import checker
from scraper.scraper import scrape
from count_proxies.count_proxies import count_proxies
import os
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def start():
    while True:
        clear_screen()
        try:
            option = input("""Proxy Checker / Scraper -

[1] Scrape Proxies
[2] Check Proxies
[3] Export Valid Proxies
[4] Proxy Count
[5] Exit

Choose An Option >> """)

            print()

            if option == '1':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                print('Starting Scrape!\n')
                scrape()
                input('Press enter to go back to the main screen...')

            elif option == '2':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                url = input('What site would you like to check the proxies against (https://example.com) >> ')
                success_key = input('What shows a valid request (<title>example</title>) >> ')
                threads = int(input('How many threads >> '))
                print()
                checker(url, success_key, threads, threads)
                print('\nProxies Finished Checking!\n')
                input('Press enter to go back to the main screen...')

            elif option == '4':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                count_proxies()
                input('Press enter to go back to the main screen...')

            elif option == '5':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                print('Exiting!')
                break

            else:
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                input('Invalid option, press enter to try again...')

        except ValueError:
            clear_screen()
            print('Proxy Checker / Scraper -\n')
            input('Invalid number entered. Press enter to try again...')

        except KeyboardInterrupt:
            print('\nExiting!')
            break

        except Exception as e:
            print(f'Error: {e}\n')

start()
