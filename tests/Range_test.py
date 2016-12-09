from timestring import Range

# added to list down the cases I tested.

#Todo- assert the tests in next commit

input_list = ['last week',
			'last 5 hours',
			'December',
			'this month',
			'last year',
			'next 2 months',
			'next 5 months',
			'last 5 months',
            'last 24 months',
            'last 16 months',
            'next 2 days']

for text in input_list:
  print(text,)
  print("===", Range(text, verbose=True, tz='Asia/Kolkata'))
