from BleachBot import BleachBot

example_bot = BleachBot('CONSUMER_KEY', 'CONSUMER_SECRET', 
					    'ACCESS_TOKEN', 'ACCESS_SECRET')

# This script will find recent tweets with either of the terms,
# process the text a little, train a simple model to predict the 
# next character given, the last 7 characters in the processed
# text, and finally use the model to produce a 10 line poem

example_bot.set_search_terms(['puppy','dog'])
example_bot.search_twitter()
example_bot.train_char_lm()
example_bot.generate_text(nletters=1000)
example_bot.generate_lines()