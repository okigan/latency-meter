run-fetch-js:
	node index-fetch.mjs -n 40 -o endpoint_latencies-js-node-fetch.csv

run-axios-js:
	node index-axios.js -n 40 -o endpoint_latencies-js-node-axios.csv

run-py:
	uv run index.py -n 40 -o endpoint_latencies-py-requests.csv