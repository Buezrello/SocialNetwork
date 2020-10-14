import clearbit, json, sys, os

clearbit.key = os.environ["CLEARBIT"]

if len(sys.argv) < 2:
	sys.exit('Usage: cli.py [email]')

email = sys.argv[1]
lookup = clearbit.Enrichment.find(email=email, stream=True)

if lookup is not None:
	print(json.dumps(lookup['person'], sort_keys=True, indent=4))
	print(json.dumps(lookup['company'], sort_keys=True, indent=4))
else:
	print('Email not found')