from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from uuid import uuid4

engine = create_engine('sqlite:///proxies.sqlite', echo=False)

base = declarative_base()

class Proxies(base):
    __tablename__ = 'proxies'

    id = Column(String(150), primary_key=True, default=str(uuid4()))
    host = Column(String(150), nullable=False)
    port = Column(Integer)
    username = Column(String(150), nullable=True)
    password = Column(String(150), nullable=True)
    site_checked_on = Column(String(150), nullable=False, default='N/A')
    http = Column(String(150), nullable=False, default='Not Checked')
    https = Column(String(150), nullable=False, default='Not Checked')
    socks4 = Column(String(150), nullable=False, default='Not Checked')
    socks5 = Column(String(150), nullable=False, default='Not Checked')
    cloudflare = Column(String(150), nullable=False, default='N/A')
    ping = Column(String(150), nullable=False, default='0 ms')
    last_checked = Column(String(150), nullable=False, default='N/A')

    def __init__(self, host, port, username, password, site_checked_on, http, https, socks4, socks5, cloudflare, ping, last_checked):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.site_checked_on = site_checked_on
        self.http = http
        self.https = https
        self.socks4 = socks4
        self.socks5 = socks5
        self.cloudflare = cloudflare
        self.ping = ping
        self.last_checked = last_checked

base.metadata.create_all(engine)