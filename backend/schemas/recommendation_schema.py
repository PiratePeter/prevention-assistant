from marshmallow import Schema, fields

class BuildingInfoSchema(Schema):
    facade = fields.String(required=True)
    basement = fields.String(required=True)
    roof = fields.String(required=True)
    heating = fields.String(required=True)

class SpecificQuestionSchema(Schema):
    question = fields.String(required=True)
    answer = fields.String(required=True)

class CustomerSchema(Schema):
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.Email(required=True)

class DamageReportSchema(Schema):
    damage = fields.String(required=True)
    damage_desc = fields.String(required=True)
    building_info = fields.Nested(BuildingInfoSchema, required=True)
    specific_questions = fields.List(fields.Nested(SpecificQuestionSchema), required=True)
    customer = fields.Nested(CustomerSchema, required=True)

    # Optional future field
    preventions = fields.String(required=False)
