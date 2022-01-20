import urllib.parse


def url_split(url):
    # For analyzing urls we usually only want the domain and the path+query
    url_obj = urllib.parse.urlparse(url)
    if url_obj.query:
        return url_obj.netloc, f"{url_obj.path}?{url_obj.query}"
    return url_obj.netloc, url_obj.path


def extract_urls(dict_or_list, dict_prefix=""):
    """
    Recurse obj and return any urls
    """
    urls = []

    def match(key, value):
        return isinstance(value, (dict, list)) or key.startswith(dict_prefix)

    def extract(obj):
        if isinstance(obj, dict):
            obj = [value for key, value in obj.items() if match(key, value)]
        if isinstance(obj, str):
            if obj.startswith("http"):
                urls.append(obj)
        elif isinstance(obj, list):
            [extract(i) for i in obj]

    extract(dict_or_list)
    return urls
