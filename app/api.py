from flask import Blueprint
from flask_restplus import Api, Resource, fields

from app.models import WorkingTimeSlot, DayOfWeek
from app.errors import InvalidUnixTime, InvalidWorkingTimeSlot
from app import utils


api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(api_v1, version='1.0', title='Opening Hours API',
          description='Opening Hours API',
          )

ns = api.namespace(
    'opening_hours', description='Convert opening hours json to human readable format')

model = api.model(
    'Opening hours',
    {'data': fields.String(required=True,
                           description="Opening hours data",
                           help="Field cannot be blank.")})


@ns.route('/convert', methods=["post"])
class OpeningHours(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @api.expect(model)
    def post(self):
        '''Convert opening hours json to human readable format'''
        json_data = api.payload
        result = _convert_opening_hours_json(json_data)

        # print result to console
        # print(result)

        return result
        


def _convert_opening_hours_json(json_data):
    working_time_slots = []
    days_of_week = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
    for i, date in enumerate(days_of_week):
        # add empty WorkingTimeSlot
        working_time_slots.append(WorkingTimeSlot(DayOfWeek.from_str(date).value, [], []))

        data = json_data[date] if date in json_data.keys() else None
        if data:
            for index, time_data in enumerate(data):
                # a restaurant might be closed in next day
                if index == 0 and time_data['type'] == 'close':
                    # append time_slot to previous date
                    working_time_slots[i - 1].appendTimeSlot(time_data['type'], time_data['value'] + utils.MAX_UNIX_TIME)
                else:
                    # append time_slot to current date
                    working_time_slots[i].appendTimeSlot(time_data['type'], time_data['value'])
    
    return [x.getReadableFormat() for x in working_time_slots]


@api.errorhandler(InvalidUnixTime)
def handle_invalid_unixtime_exception(error):
    '''Return error message and 400 status code'''
    return {'message': error.message}, 400


@api.errorhandler(InvalidWorkingTimeSlot)
def handle_invalid_workingtimeslot_exception(error):
    '''Return error message and 400 status code'''
    return {'message': error.message}, 400
