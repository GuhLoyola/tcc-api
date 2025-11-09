import re
import string
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException
import pandas as pd
from urllib.parse import urlparse

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def is_valid_url(url: str) -> bool:
    try:
        if url.startswith(("http://", "https://")):
            url = re.sub(r"^https?://", "", url)
        test_url = url if '://' in url else 'http://' + url
        result = urlparse(test_url)
        return all([result.scheme, result.netloc])
    except:
        return False
    
def extract_features(url: str) -> pd.DataFrame:
    features = {}

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    if not url.endswith("/"):
        url += "/"

    parsed_url = None
    try:
        parsed_url = urlparse(url)
        netloc = parsed_url.netloc
        tld = netloc.split('.')[-1] if '.' in netloc else ''
    except Exception:
        tld = ''
        netloc = ''
    
    features['url_length'] = len(url)
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_special_chars'] = sum(c in string.punctuation for c in url)
    features['num_subdomains'] = netloc.count('.') - 1 if netloc else 0
    features['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', netloc)))
    features['num_params'] = url.count('?')
    features['num_fragments'] = url.count('#')
    features['num_slashes'] = url.count('/')
    features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))
    features['tld_length'] = len(tld)
    features['is_common_tld'] = int(tld in ['com','org','net','edu','gov'])
    features['has_hex'] = int(bool(re.search(r'%[0-9a-fA-F]{2}', url)))
    features['repeated_chars'] = int(bool(re.search(r'(.)\1{3,}', url)))
    
    return pd.DataFrame([features])

def check_url_status(url: str) -> int:
    TIMEOUT = 5
    try:
        response = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
        
        if response.status_code == 200:
            return 1
        return -1
    except (ConnectionError, Timeout, TooManyRedirects, RequestException):
        return 0
    except Exception:
        return 0
        