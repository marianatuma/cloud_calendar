#!flask/bin/python
from flask import Flask , jsonify, abort, make_response, request, url_for
import datetime

app = Flask(__name__)

#Creating memory array
globalCalendarName = ''
calendar_list = []
calendar = [
    {
        'id': 1,
        'date': u'20-04-2014',
        'startTime': u'08:00',
        'endTime': u'10:00',
        'description': u'Study machine learning', 
        'repeats': None
    },
    {
        'id': 2,
        'date': u'20-03-2014',
        'startTime': u'08:00',
        'endTime': u'11:00',
        'description': u'BigData meetup', 
        'repeats': None
    },
    {
        'id': 3,
        'date': u'11-05-2014',
        'startTime': u'20:00',
        'endTime': u'22:00',
        'description': u'Arctic Monkeys show', 
        'repeats': None
    }
]

calendar_dic = {'basicCalendar': calendar}

calendar_list.append(calendar_dic)

#Getting all calendars
@app.route('/', methods = ['GET'])
def get_calendars():
    return jsonify( { 'calendars': calendar_list } )

#Creating a calendar
@app.route('/', methods = ['POST'])
def create_calendar():
    new_calendar = { request.json['calendarName']: [{}] } 
    calendar_list.append(new_calendar)
    return jsonify( { 'calendar': new_calendar } ), 201

#Getting all events
@app.route('/<calendarName>', methods = ['GET'])
def get_events(calendarName):
    exp_calendar = searchCalendar(calendar_list, calendarName)
    globalCalendarName = calendarName  #little trashy code because of map() function
    return jsonify( { calendarName: map(make_public_task, exp_calendar) } )
    #return jsonify( { calendarName: exp_calendar } )
    
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], calendarName = globalCalendarName, _external = True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/<calendarName>/<earlierLimit>/<laterLimit>', methods = ['GET'])
def get_events_by_range_date(calendarName,earlierLimit,laterLimit):
    exp_calendar = searchCalendar(calendar_list, calendarName);
    result_calendar = []
    for event in exp_calendar:
      eventDate = event.get("date")
      print("Looking for date")
      if check_if_within_range(earlierLimit,eventDate,laterLimit):
        result_calendar.append(event)
    return jsonify( { calendarName: result_calendar } )

def searchCalendar(list, calName):
    for item in list:
        if item.get(calName):
            return item[calName]

#Posting a event
@app.route('/<calendarName>', methods = ['POST'])
def create_events(calendarName):
    if not request.json: #handle errors
        abort(400)
    event = {
        'id': calendar[-1]['id'] + 1,
        'date': request.json['date'],
        'startTime': request.json['startTime'],
        'endTime': request.json['endTime'],
        'description': request.json.get('description', ""),
        'repeats': request.json.get('repeats',None)
    }
    exp_calendar = searchCalendar(calendar_list, calendarName);
    exp_calendar.append(event)
    #here two lines of code just to get the {} off of the new calendars, because now will be some content there
    if exp_calendar[0]=={}:
      exp_calendar.remove({})
    #
    return jsonify( { 'event': event } ), 201

#date will be inserted as dd-mm-yyyy
def date_parser(dateString):
	date_struct = datetime.datetime.strptime(dateString, "%d-%m-%Y").date()
	return date_struct

def check_if_within_range(earlierLimit, date, laterLimit):
  earlier = date_parser(earlierLimit)
  later = date_parser(laterLimit)
  date = date_parser(date)

  if earlier <= date <= later :
    return True
  else :
    return False
  
#Getting a specific event
@app.route('/<calendarName>/<int:task_id>', methods = ['GET'])
def get_task(calendarName,task_id):
    exp_calendar = searchCalendar(calendar_list, calendarName);
    event = filter(lambda t: t['id'] == task_id, exp_calendar)
    if len(event) == 0:
        abort(404)
    return jsonify( { 'event': event[0] } )

#Changing a event
@app.route('/<calendarName>/<int:event_id>', methods = ['PUT'])
def update_event(calendarName,event_id):
    exp_calendar = searchCalendar(calendar_list, calendarName);
    event = filter(lambda t: t['id'] == event_id, exp_calendar )
    if len(event) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'date' in request.json and type(request.json['date']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'startTime' in request.json and type(request.json['startTime']) is not unicode:
        abort(400)
    if 'endTime' in request.json and type(request.json['endTime']) is not unicode:
        abort(400)

    event[0]['date'] = request.json.get('date', event[0]['date'])
    event[0]['description'] = request.json.get('description', event[0]['description'])
    event[0]['startTime'] = request.json.get('startTime', event[0]['startTime'])
    event[0]['endTime'] = request.json.get('endTime', event[0]['endTime'])
    return jsonify( { 'event': event[0] } )

#Deleting a event
@app.route('/<calendarName>/<int:event_id>', methods = ['DELETE'])
def delete_event(calendarName,event_id):
    exp_calendar = searchCalendar(calendar_list, calendarName);
    event = filter(lambda t: t['id'] == event_id, exp_calendar)
    if len(event) == 0:
        abort(404)
    exp_calendar.remove(event[0])
    return jsonify( { 'result': True } )

@app.route('/<calendarName>', methods = ['DELETE'])
def delete_calendar(calendarName):
    for cal in calendar_list:
      if cal.get(calendarName):
        calendar_list.remove(cal)
    return jsonify( { 'result': True } )
  
#Handling error returning JSON
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=3000)