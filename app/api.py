from flask import Blueprint
from flask_restplus import Api, Resource, fields


api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(api_v1, version='1.0', title='Openning Hours API',
          description='Openning Hours API',
          )

ns = api.namespace(
    'openning_hours', description='Convert opening hours json to human readable format')

model = api.model(
    'Openning hours',
    {'data': fields.String(required=True,
                           description="Openning hours data",
                           help="Field cannot be blank.")})


@ns.route('/convert', methods=["post"])
class OpenningHours(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @api.expect(model)
    def post(self):
        '''Convert opening hours json to human readable format'''
        json_data = api.payload

        result = ''

        days_of_week = list(json_data.keys())
        for date in days_of_week:
            data = json_data[date]
            if data is None or len(data) == 0:
                print(date.capitalize() + ': Closed')
            else:
                print(data)
