from marshmallow import Schema, fields
import valideer as V
import valideer.base

from nayami.common.error import ValidationError

post = {
    "+content": V.String(min_length=0),
    "+sender": V.String(),
    "+sender_email": V.String(),
}

reply = {
    "+content": V.String(min_length=0),
    "+sender_email": V.String(),
}


class BaseSchema(Schema):
    def handle_error(self, exc, data):
        raise ValidationError(msg=exc.messages)


class PostSchema(BaseSchema):
    id = fields.Str(dump_only=True)
    content = fields.Str(required=True)
    recipient = fields.Str(dump_only=True)
    sender = fields.Str(required=True)
    sender_email = fields.Str(required=True)
    reply_id = fields.Str(dump_only=True)
    create_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+08:00')

    def to_dict(self, data):
        validator = V.parse(post)
        try:
            validator.validate(data)
        except valideer.base.ValidationError as e:
            raise ValidationError(e.msg)
        return self.load(data).data


class ReplySchema(BaseSchema):
    content = fields.Str(required=True)
    sender_email = fields.Str(required=True)
    create_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+08:00')

    def to_dict(self, data):
        validator = V.parse(reply)
        try:
            validator.validate(data)
        except valideer.base.ValidationError as e:
            raise ValidationError(e.msg)
        return self.load(data).data
