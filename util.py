import cloudscraper
import requests
from sqlalchemy.orm import sessionmaker
import models
import json
import re

Session = sessionmaker(bind=models.engine)
session = Session()

def scrape(provider, prot: str, log=print):
    proxies = []

    pattern = r'://([\d\.]+:\d+)|^([\d\.]+:\d+)'
    
    with open('sources.json', 'r') as f:
        sources = json.load(f)

    if provider != 'all':
        for source in sources['sources']:
            proxies = []

            if source['name'] == provider:
                if prot != 'all':
                    log(f"[INFO] Starting Scrape! | [SOURCE] {source['name']} | [PROTOCOL] {prot.upper()}")

                    if source['protocols'][prot] == None:
                        log(f"[WARN] Not Available! | [SOURCE] {source['name']} | [PROTOCOL] {prot.upper()}")
                    else:
                        with requests.Session() as session:
                            resp = session.get(source['protocols'][prot])
                            cleaned = resp.text.replace(' ', '_')

                            for line in cleaned.split():
                                match = re.search(pattern, line)
                                if match:
                                    host_port = match.group(1) or match.group(2)
                                    proxies.append(host_port)

                            log(f"[INFO] Scraped {len(list(set(proxies)))} Unique Proxies! | [SOURCE] {source['name']} | [PROTOCOL] {prot.upper()}")
                            del proxies

                    log(" ")
                else:
                    for protocol in source['protocols']:
                        proxies = []

                        log(f"[INFO] Starting Scrape! | [SOURCE] {source['name']} | [PROTOCOL] {protocol.upper()}")

                        if source['protocols'][protocol] is None:
                            log(f"[WARN] Not Available! | [SOURCE] {source['name']} | [PROTOCOL] {protocol.upper()}")
                        else:
                            with requests.Session() as session:
                                resp = session.get(source['protocols'][protocol])
                                cleaned = resp.text.replace(' ', '_')

                                for line in cleaned.split():
                                    match = re.search(pattern, line)
                                    if match:
                                        host_port = match.group(1) or match.group(2)
                                        proxies.append(host_port)

                                log(f"[INFO] Scraped {len(list(set(proxies)))} Unique Proxies! | [SOURCE] {source['name']} | [PROTOCOL] {protocol .upper()}")
                                del proxies

                        log(" ")
    else:
        for source in sources['sources']:
            proxies = []

            log(f"[INFO] Starting Scrape! | [SOURCE] {source['name']} | [PROTOCOL] {prot.upper()}")
            
            if prot != 'all':
                if source['protocols'][prot] == None:
                    log(f"[WARN] Not Available! | [SOURCE] {source['name']} | [PROTOCOL] {prot.upper()}")
                else:
                    with requests.Session() as session:
                        resp = session.get(source['protocols'][prot])
                        cleaned = resp.text.replace(' ', '_')

                        for line in cleaned.split():
                            match = re.search(pattern, line)
                            if match:
                                host_port = match.group(1) or match.group(2)
                                proxies.append(host_port)

                        log(f"[INFO] Scraped {len(list(set(proxies)))} Unique Proxies! | [SOURCE] {source['name']} | [PROTOCOL] {prot.upper()}")
                        del proxies

                log(" ")
            else:
                for protocol in source['protocols']:
                    log(source['protocols'][protocol])
