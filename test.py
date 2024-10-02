import requests
import json
import retrieve_token

# Application Constants
RDP_version = "/v1"
base_URL = "https://api.refinitiv.com"
category_URL = "/data/historical-pricing"
endpoint_URL = "/views/interday-summaries"
universe_parameter_URL = "/"

def prettyPrintData(vData):
	#print(json.dumps(vData, indent=2))

	line = ""
	for i in vData["headers"]:
		line = line + i["name"] + ", "
	line = line [:-2]
	print(line)
	
	print("---------------")

	for d in vData["data"]:
		line = ""
		for pt in d:
			line = line + str(pt) + ", "
		line = line [:-2]
		print(line)


if __name__ == "__main__":
	# Get latest access token
	print("Getting OAuth access token...")
	accessToken = retrieve_token.get_token()
	print("Invoking data request")

	# Make data request
	RIC="IBM.N"

	RESOURCE_ENDPOINT = base_URL + category_URL + RDP_version + endpoint_URL + universe_parameter_URL + RIC

	requestData = {
		"interval": "P1D",
		"start": "2018-02-01",
		"end": "2018-05-05",
		"adjustments": "exchangeCorrection,manualCorrection,CCH,CRE,RPO,RTS",
		"maxpoints": 20,
		"fields": "BID,ASK,OPEN_PRC,HIGH_1,LOW_1,TRDPRC_1,NUM_MOVES,TRNOVR_UNS"
	}

	dResp = requests.get(RESOURCE_ENDPOINT, headers = {"Authorization": "Bearer " + accessToken}, params = requestData)

	if dResp.status_code != 200:
		print("Unable to get data. Code %s, Message: %s" % (dResp.status_code, dResp.text))
	else:
		print("Resource access successful")
		# Display data
		jResp = json.loads(dResp.text)
		prettyPrintData(jResp[0])