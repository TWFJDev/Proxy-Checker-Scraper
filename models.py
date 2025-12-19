from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base
from uuid import uuid4

engine = create_engine('sqlite:///proxies.db', echo=False)

base = declarative_base()

def gen_uuid():
    return str(uuid4())

class Proxies(base):
    __tablename__ = 'proxies'

    id = Column(String(150), primary_key=True, default=lambda: gen_uuid())
    host = Column(String(150), nullable=True)
    port = Column(Integer)
    username = Column(String(150), nullable=True)
    password = Column(String(150), nullable=True)
    site_checked_on = Column(String(150), nullable=True, default=None)
    http = Column(Boolean, nullable=True, default=False)
    https = Column(Boolean, nullable=True, default=False)
    socks4 = Column(Boolean, nullable=True, default=False)
    socks4a = Column(Boolean, nullable=True, default=False)
    socks5 = Column(Boolean, nullable=True, default=False)
    socks5h = Column(Boolean, nullable=True, default=False)
    last_checked = Column(String(150), nullable=True, default=None)

    def __init__(self, host, port, username, password, site_checked_on, http, https, socks4, socks4a, socks5, socks5h, last_checked):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.site_checked_on = site_checked_on
        self.http = http
        self.https = https
        self.socks4 = socks4
        self.socks4a = socks4a
        self.socks5 = socks5
        self.socks5h = socks5h
        self.last_checked = last_checked

base.metadata.create_all(engine)