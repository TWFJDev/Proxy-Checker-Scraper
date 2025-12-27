import models, requests, random
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED

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

def get_random_proxy():
    with get_session() as session:
        total = session.query(models.Proxies.id).count()
        offset = random.randint(0, total - 1)

        proxy = (
            session.query(models.Proxies)
            .offset(offset)
            .limit(1)
            .first()
        )

        session.expunge(proxy)
        return proxy

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
        "proxy": f"{host}:{port}",
        "site_checked_on": site_url,
        "http": check_proxy(site_url, success_key, host, port, "http"),
        "https": check_proxy(site_url, success_key, host, port, "https"),
        "socks4": check_proxy(site_url, success_key, host, port, "socks4"),
        "socks4a": check_proxy(site_url, success_key, host, port, "socks4a"),
        "socks5": check_proxy(site_url, success_key, host, port, "socks5"),
        "socks5h": check_proxy(site_url, success_key, host, port, "socks5h")
    }

def proxy_check_future(site_url, success_key):
    proxy = get_random_proxy()
    if not proxy:
        return False

    results = check_proxy_all_types(
        site_url,
        success_key,
        proxy.host,
        proxy.port
    )

    return results

def run_checks(
    site_url,
    success_key,
    protocol,
    goal_count,
    workers
):
    found = 0
    results = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = set()

        for _ in range(workers):
            futures.add(
                executor.submit(
                    proxy_check_future,
                    site_url,
                    success_key
                )
            )

        while futures and found < goal_count:
            done, futures = wait(
                futures,
                return_when=FIRST_COMPLETED
            )

            for future in done:
                result = future.result()

                try:
                    if result[protocol.lower()] == True:
                        found += 1
                        print(f"[+] {protocol.upper()} valid ({found}/{goal_count})")
                        results.append(result)
                    else:
                        pass
                except Exception:
                    pass

                if found < goal_count:
                    futures.add(
                        executor.submit(
                            proxy_check_future,
                            site_url,
                            success_key
                        )
                    )
                else:
                    for f in futures:
                        f.cancel()
                    futures.clear()
                    break

    print(f"\nFinished: {found} {protocol.upper()} proxies found")
    return results