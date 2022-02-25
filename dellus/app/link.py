from dellus.config import config
from dellus.core.hashdigest import HashDigest
from dellus.exception import URLNotFound, URLAuthFailed
from dellus.exception.error import LinkExpired
from dellus.model.link import LinkManager
from dellus.utilities.urls import get_short_path
from dellus.validator.link import LinkSchema


def shorten(long_url, short_code=None, expire_after=None, description=None,
            secret_key=None, owner=None, request=None):
   
    url_manager = LinkManager()
    query_dict = dict(long_url=long_url, is_custom=False, is_protected=False)
    insert_dict = query_dict
    if short_code:
        query_dict.update(dict(short_code=short_code, is_custom=True))
        insert_dict = query_dict
    if secret_key:
        query_dict.update(secret_key=str(secret_key), is_protected=True)
        insert_dict = query_dict
    if expire_after:
        insert_dict['expire_after'] = expire_after
    urlobj = url_manager.find(**query_dict)
    if urlobj is None:
        url_manager.add(**insert_dict)
    if request:
        return url_manager.link
    return LinkSchema().dump(url_manager.link).data


def unshorten(short_url, secret_key=None,
              query_by_code=True, request=None):
    
    url_manager = LinkManager()
    short_path = get_short_path(short_url)
    if query_by_code is True:
        query_dict = dict(short_code=short_path)
    else:
        _id = HashDigest().decode(short_path)
        query_dict = dict(id=_id)
    link = url_manager.find(**query_dict)
    if link is None:
        raise URLNotFound(short_url)
    if url_manager.has_expired():
        raise LinkExpired
    if link.is_protected:
        if not secret_key or str(link.secret_key) != str(secret_key):
            raise URLAuthFailed(short_url)
    if request:
        return link
    return LinkSchema().dump(link).data


def resolve_short(short_code, request=None, secret_key=None):
   
    manager = LinkManager()
    link = manager.get_by_code(short_code=short_code)
    assert link is not None
    if manager.has_expired() is True:
        raise LinkExpired('Link has expired')
    if link.is_protected:
        if not secret_key or str(link.secret_key) != str(secret_key):
            raise URLAuthFailed(short_code)
   
    return link.long_url