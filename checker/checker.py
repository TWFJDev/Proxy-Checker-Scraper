import cloudscraper, models, requests
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def check_proxy(site_url, success_key, host, port, proxy_type="http", timeout=5):
    url = site_url

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    
    if proxy_type in ["http", "https"]:
        proxies = {proxy_type: f"http://{host}:{port}"}
    elif proxy_type in ["socks4", "socks4a", "socks5", "socks5h"]:
        proxies = {
            "http": f"{proxy_type}://{host}:{port}",
            "https": f"{proxy_type}://{host}:{port}"
        }
    else:
        raise ValueError(f"Unsupported proxy type: {proxy_type}")

    try:
        with requests.Session() as session:
            resp = session.get(url, proxies=proxies, headers={'User-Agent': user_agent}, timeout=timeout)

            if success_key in resp.content.decode('utf-8'):
                return True
            else:
                return False
    except Exception:
        return False

def check_proxy_all_types(site_url, success_key, host, port):
    return {
        "site_checked_on": site_url,
        "http": check_proxy(site_url, success_key, host, port, "http"),
        "https": check_proxy(site_url, success_key, host, port, "https"),
        "socks4": check_proxy(site_url, success_key, host, port, "socks4"),
        "socks4a": check_proxy(site_url, success_key, host, port, "socks4a"),
        "socks5": check_proxy(site_url, success_key, host, port, "socks5"),
        "socks5h": check_proxy(site_url, success_key, host, port, "socks5h")
    }

def checker(site_url, success_key, workers, batch):
    last_id = 0

    while True:
        with get_session() as session:
            proxies_list = (session.query(models.Proxies.id, models.Proxies.host, models.Proxies.port).filter(models.Proxies.id > last_id).order_by(models.Proxies.id).limit(batch).all())

            if not proxies_list:
                break

            updates = []

            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_to_proxy = {executor.submit(check_proxy_all_types, site_url, success_key, host, port): (proxy_id, host, port) for proxy_id, host, port in proxies_list}

                for future in as_completed(future_to_proxy):
                    proxy_id, host, port = future_to_proxy[future]

                    try:
                        result = future.result()
                    except Exception:
                        result = {"http": False, "https": False, "socks4": False, "socks4a": False, "socks5": False, "socks5h": False}

                    updates.append({"id": proxy_id, **result, "last_checked": datetime.now(timezone.utc)})

                    print(f"{host}:{port}", result)

            if updates:
                session.bulk_update_mappings(models.Proxies, updates)
                session.commit()

            last_id = proxies_list[-1][0]

# url = "https://crunchyroll.com"
# success_key = "<title>Crunchyroll"
# url = 'https://ip-api.com/'
# success_key = '<title>IP-API.com - Geolocation API</title>'
# workers = 100
# batch = 50

# checker(
#     url,
#     success_key,
#     workers,
#     batch
# )