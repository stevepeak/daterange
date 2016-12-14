from timestring import Range

# added to list down the cases I tested.

#Todo- assert the tests in next commit

input_list = [
	'from january 10th 2010 to jan 20th 2010',
	'from jan 10 2016 5 am to 9 am', # fails
    'from jan 10 2016 5 am to jan 10, 2016 9 am',
	'from 2 PM to 4PM',
	'last week',
	'last 5 hours',
	'next 4 hours',
	'December',
	'this month',
	'last year',
	'next 2 months',
	'next 5 months',
	'last 5 months',
	'last 24 months',
	'last 16 months',
	'next 2 days',
	'tomorrow',
	'upcoming week',
	'upcoming month'
 ]

for text in input_list:
  print(text),
  print("===", Range(text, verbose=False, tz='Asia/Kolkata'))
