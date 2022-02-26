import string

from datetime import datetime
from marshmallow import Schema, fields, post_dump, ValidationError

from dellus.utilities.urls import make_short_url, validate_url
from dellus.utilities.utils import make_url_from_id


VALID_INPUT_CHARS = string.ascii_letters + string.digits
SECRET_KEY_ERROR = "Max allowed length for secret key is between 1-8"
INVALID_CUSTOM_CODE_ERROR = "Invalid input. Length should be <= 8 and should" \
                            " be a valid alphabat, digit or a mix of both"
MAX_SHORT_CODE_LEN = 8


# Custom validators
def is_valid_custom_code_or_secret(code):  
    if len(code) > MAX_SHORT_CODE_LEN:
        raise ValidationError(INVALID_CUSTOM_CODE_ERROR)
    for c in code:
        if c not in VALID_INPUT_CHARS:
            raise ValidationError(INVALID_CUSTOM_CODE_ERROR)
    return True


class LinkSchema(Schema):
    id = fields.Method('create_id_link', dump_only=True)
    long_url = fields.URL(required=True, validate=validate_url)
    short_code = fields.Str(required=False,
                            allow_none=True,
                            validate=is_valid_custom_code_or_secret)
    short_url = fields.Method('short_url_path', dump_only=True)
    description = fields.Str(required=False, allow_none=True)
    secret_key = fields.Str(required=False,
                            allow_none=True,
                            validate=is_valid_custom_code_or_secret)
    expire_after = fields.Int(required=False, allow_none=True)
    is_protected = fields.Bool(default=False, required=False, allow_none=True)
    is_disabled = fields.Bool(default=False, required=False)
    is_custom = fields.Bool(default=False, required=False)
    owner = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updated_at = fields.DateTime()

    def short_url_path(self, link):
        if link and link.short_code:
            return make_short_url(link.short_code)

    def create_id_link(self, link):
        if link and link.id:
            return make_url_from_id(link.id, 'link')

    @post_dump
    def format_data(self, data):
        if data and data.get('owner'):
            data['owner'] = make_url_from_id(data['owner'], 'user')
        if data and data.get('created_at'):
            data['created_at'] = datetime.strptime(
                data['created_at'], '%Y-%m-%d %H:%M:%S'
            ).strftime('%d %b, %Y %H:%M:%S')
        return data
