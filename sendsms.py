from twilio.rest import Client
def send(b) :
	account_sid = "AC2eefe373e1d8447c1a39d266d93cb589"
	auth_token  = "ae238bc480d1c302e1091f2b6d45d6d2"
	client = Client(account_sid, auth_token)
	message = client.messages.create(
		to="+917411986638", 
		from_="+15632656818 ",
		body=b)

	print(message.sid)