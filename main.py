from checker.checker import checker
from scraper.scraper import scrape
from count_proxies.count_proxies import count_proxies
from export_proxies.export_proxies import run_checks
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
[2] Export Valid Proxies
[3] Proxy Count
[4] Exit

Choose An Option >> """)

            print()

            if option == '1':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                print('Starting Scrape!\n')
                scrape()
                input('Press enter to go back to the main screen...')

            # elif option == '2':
            #     clear_screen()
            #     print('Proxy Checker / Scraper -\n')
            #     url = input('What site would you like to check the proxies against (https://example.com) >> ')
            #     success_key = input('What shows a valid request (<title>example</title>) >> ')
            #     threads = int(input('How many threads >> '))
            #     print()
            #     checker(url, success_key, threads, threads)
            #     print('\nProxies Finished Checking!\n')
            #     input('Press enter to go back to the main screen...')

            elif option == '2':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                site_url = input('What site would you like to check the proxies against (https://example.com) >> ')
                success_key = input('What shows a valid request (<title>example</title>) >> ')
                protocols = "Choose a protocol:\n[1] HTTP\n[2] HTTPS\n[3] SOCKS4\n[4] SOCKS4A\n[5] SOCKS5\n[6] SOCKS5H"
                print(protocols)
                protocol = input('Option >> ')
                if protocol == '1':
                    protocol_final = 'http'
                elif protocol == '2':
                    protocol_final = 'https'
                elif protocol == '3':
                    protocol_final = 'socks4'
                elif protocol == '4':
                    protocol_final = 'socks4a'
                elif protocol == '5':
                    protocol_final = 'socks5'
                elif protocol == '6':
                    protocol_final = 'socks5h'
                goal_count = int(input('How many proxies would you like to export >> '))
                threads = int(input('How many threads >> '))
                print()
                print('Starting Check! (If proxy is valid info will print)\n')
                results = run_checks(site_url, success_key, protocol_final, goal_count, threads)
                input('\nPress enter to go back to the main screen...')

            elif option == '3':
                clear_screen()
                print('Proxy Checker / Scraper -\n')
                count_proxies()
                input('Press enter to go back to the main screen...')

            elif option == '4':
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
            print('Proxy Checker / Scraper -\n')
            print(f'Error: {e}. Press enter to try again...')

start()