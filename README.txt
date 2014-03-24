Students:
Michel Siqueira Reis
Mariana Tuma Athayde

Cloud URL: http://cloudcomputingassignment.herokuapp.com/

Document usage:

	The API supports multiple calendars, that support multiple events each. It comes with one built in calendar that is called "basicCalendar" that comes with 3 events for testing purposes.

	The inputs in this document will be represented like <this>.

	Structure for requests:
		GET
			'/'  >> 						Returns a JSON object with all calendars
			'/<calendarName>' >> 			Returns a JSON object with the events of the specific calendar
			'/<calendarName>/<eventId>' >>	Returns a JSON object with a specific event of a specific calendar
			'/<calendarName>/<earlierLimit>/<laterLimit>'  >>  Return a list of events in the range of dates provided for the specific calendar

		POST
			'/'  >>							Creates a calendar
				JSON Structure: 			{ "calendarName": <calendarName> }

			'/<calendarName>' >> 			Create an event for a specific calendar
				JSON Structure:				{ "date":"<01-01-2015>","startTime":"<09:00>",
											"description":"<Description>","endTime":"<10:00>","repeats":"<Time>" }

		PUT
			'/<calendarName>/<eventId>' >>	Changes a event in a specific calendar
				JSON Structure:				{ "date":"<01-01-2015>","startTime":"<09:00>",
											"description":"<Description>","endTime":"<10:00>","repeats":"<Time>" }

		DELETE
			'/<calendarName>' >> 			Deletes a calendar
			'/<calendarName>/<eventId>'  >> Deletes a event in a specific calendar

	It's important not to misspell the "date" structure "DD-MM-YYYY", for parsing purposes


 

