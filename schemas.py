from marshmallow import Schema, fields, validate

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True) 
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    store_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    contact_number = fields.Str()
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str()
    phone_number = fields.Int()
    date_of_birth = fields.Date(required=True, format="%Y-%m-%d")
    email = fields.Email()

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class SiteSchema(Schema):
    site_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    status = fields.Str()

class DeviceSchema(Schema):
    device_id = fields.Int(required=True, dump_only=True)
    site_id = fields.Int(required=True)
    device_name = fields.Str(required=True)
    device_url = fields.Str(required=True, load_only=True)
    last_seen = fields.DateTime()

class DeviceConfigSchema(Schema):
    location_id = fields.Int()
    new_targets = fields.Int() 
    function_code = fields.Str()

class ProductionPlanItemSchema(Schema):
    sequence = fields.Int(required=True)
    part_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    created_by = fields.Int(required=True)

class ProductionPlanSchema(Schema):
    data = fields.List(
        fields.Nested(ProductionPlanItemSchema),
        required=True,
        validate=validate.Length(min=1)
    )