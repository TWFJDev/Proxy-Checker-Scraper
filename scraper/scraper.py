from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import models, json, requests, re

SessionLocal = sessionmaker(bind=models.engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_source_urls():
    urls = []
    with open('sources.json', 'r') as f:
        lines = json.load(f)

        for line in lines['sources']:
            for protocol, url in line['protocols'].items():
                if url:
                    urls.append(url)

    return urls

def scrape():
    urls = get_source_urls()
    pattern = re.compile(r'://([\d\.]+:\d+)|^([\d\.]+:\d+)')

    print(f'Scraping Proxies From {len(urls)} URLs!\n')

    with get_session() as session:
        existing_proxies = {(p.host, p.port) for p in session.query(models.Proxies.host, models.Proxies.port)}

        i = 1

        for url in urls:
            with requests.Session() as req:
                print(f'[{i}/{len(urls)}] | {url}')

                i += 1

                try:
                    resp = req.get(url)
                    resp.raise_for_status()
                except requests.RequestException:
                    print(f"Failed to fetch {url}")
                    continue

                for proxy in resp.text.split():
                    line = proxy.strip().replace(' ', '_')
                    match = pattern.search(line)
                    if not match:
                        continue

                    proxy_match = match.group(1) or match.group(2)
                    host, port = proxy_match.split(':')

                    if (host, int(port)) in existing_proxies:
                        continue
                    
                    if int(port) <= 65535:
                        new_proxy = models.Proxies(
                            host=host,
                            port=int(port),
                            username=None,
                            password=None,
                            site_checked_on=None,
                            http=None,
                            https=None,
                            socks4=None,
                            socks4a=None,
                            socks5=None,
                            socks5h=None,
                            last_checked=None
                        )

                        session.add(new_proxy)
                        existing_proxies.add((host, int(port)))

        print("\nInserting Proxies Into DB!")

    print("\nFinished Scraping!\n")


# scrape()