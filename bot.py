import json
import requests
import sys

class Bot:
	def __init__(self, api_token, api_url, api_bot_id):
		self.api_token = api_token
		self.api_url = api_url
		self.api_bot_id = api_bot_id

	def start(self):
		api_endpoint = "servers/"
		response = self.get(api_endpoint)
		if response['status'] != 200:
			sys.exit("Cannot get " + api_endpoint)

		servers = response['body']
		
		for server in servers:
			server_url = server['protocol']['slug'] + "://" + server['hostname']

			api_endpoint = "servers/" + str(server['id']) + "/endpoints/"
			response = self.get(api_endpoint)
			if response['status'] != 200:
				sys.exit("Cannot get " + api_endpoint)

			endpoints = response['body']

			for endpoint in endpoints:
				url = server_url + endpoint['url']

				response = requests.get(url)
				data = {
					'response_code': response.status_code,
					'response_time': response.elapsed.total_seconds(),
					'response_headers': str(response.headers),
					'response_body': response.text,
					'bot_id': self.api_bot_id,
				}

				api_endpoint = "servers/" + str(server['id']) + "/endpoints/" + str(endpoint['id']) + "/pings/"
				response = self.post(api_endpoint, data)

				if response['status'] != 201:
					sys.exit("Cannot post " + api_endpoint)


	def get(self, endpoint):
		headers = {
			'Authorization': 'Token ' + self.api_token,
		}

		response = requests.get(self.api_url + endpoint, headers=headers)

		return {
			'status': response.status_code,
			'body': json.loads(response.text),
		}


	def post(self, endpoint, data):
		headers = {
			'Authorization': 'Token ' + self.api_token,
		}

		response = requests.post(self.api_url + endpoint, headers=headers, data=data)

		return {
			'status': response.status_code,
			'body': json.loads(response.text),
		}


if __name__ == "__main__":
	print("This is not made to be called, please run app.py")