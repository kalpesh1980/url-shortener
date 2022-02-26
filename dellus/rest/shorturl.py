from flask import request, redirect, abort, jsonify
from flask.views import MethodView

from dellus.app.auth import APITokenAuth
from dellus.app.link import unshorten, resolve_short
from dellus.exception import URLNotFound, URLAuthFailed
from dellus.exception.error import LinkExpired, ShortURLUnavailable
from dellus.model import LinkManager, UserManager
from dellus.validator import LinkSchema
from dellus.utilities.urls import validate_url
from dellus.core.logger import log


class LongUrlApi(MethodView):
    """View for handeling long url operations."""
    schema = LinkSchema()
    manager = LinkManager()

    def get(self):
        """Return data if long url already exists."""
        long_url = request.args.get('url')
        is_valid = validate_url(long_url)
        if is_valid is False:
            return jsonify(dict(error='Invalid URL.')), 400
        link = self.manager.get(long_url)
        if self.manager.has_expired():
            return jsonify(dict(error="Link has expired")), 404
        if link is None:
            abort(404)
        result = self.schema.dump(link)
        return jsonify(result.data), 200

    @APITokenAuth.token_optional
    def post(self):
        payload = request.get_json()
        data, errors = self.schema.load(payload)

        if errors:
            log.error('Error in the request payload %s', errors)
            if errors.get('long_url'):
                errors.update({'error': errors.get('long_url')})
            return jsonify(errors), 400

        # if authenticated request check valid user
        user_email = APITokenAuth.get_jwt_identity()
        if user_email:
            user = UserManager().find(email=user_email)
            if not user:
                return jsonify(dict(error='Invalid user')), 400
            data['owner'] = user.id

        long_url = data.pop('long_url')
        log.info('Shortening url %s', long_url)
        link = self.manager.get(long_url)
        if link is None or (
                        data.get('is_custom') or
                        data.get('is_protected') or
                        data.get('expire_after')):
            try:
                link = self.manager.add(long_url, **data)
            except ShortURLUnavailable as e:
                return jsonify(dict(error=str(e))), 400
        result = self.schema.dump(link)
        log.info('Url: %s shortened, response: %s', long_url, result.data.get('short_code'))
        return jsonify(result.data), 201


class ShortURLApi(MethodView):
   
    schema = LinkSchema()

    def get(self):
        secret = request.headers.get('secret_key')
        short_url = request.args.get('url')
        try:
            long_url = unshorten(short_url, secret_key=secret,
                                 query_by_code=True, request=request)
            result = self.schema.dump(long_url)
        except LinkExpired:
            return jsonify(dict(error="Link has expired")), 410
        except URLAuthFailed:
            return jsonify(dict(error="Secret key not provided")), 403
        except URLNotFound:
            return jsonify(
                dict(error="URL Not Found Or Expired")), 404
        return jsonify(result.data), 200


@APITokenAuth.token_optional
def resolve(code):
    """Resolve the short url. code=301 PERMANENT REDIRECTION"""
    secret_key = request.headers.get('secret_key')
    try:      
        long_url = resolve_short(
        code.strip('+'), request=request, secret_key=secret_key)
        response = redirect(long_url, code=301)
    except LinkExpired:
        response = jsonify(dict(error="Link has expired")), 404
    except URLAuthFailed:
        response = jsonify({'error': 'Access to URL forbidden'}), 403
    except (URLNotFound, AssertionError):
        response = jsonify({'error': 'URL not found or disabled'}), 404
    return response


def dummy():
    return '', 204
