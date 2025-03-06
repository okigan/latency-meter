// index.mjs (or index.js if you set "type": "module" in package.json)
import fetch from 'node-fetch';
import https from 'https';
import fs from 'fs';
import { performance } from 'perf_hooks';
import minimist from 'minimist';

const args = minimist(process.argv.slice(2), {
  alias: { n: 'iterations', o: 'output' },
  default: { iterations: 40, output: 'endpoint_latencies.csv' }
});

// Create an HTTPS agent with keep-alive enabled
const httpsAgent = new https.Agent({ keepAlive: true });

// List of endpoints with provider names
const endpoints = [
  { provider: "Crunchyroll", url: "https://prd.partner.crunchyroll.com/api/core/healthcheck" },
  { provider: "Google", url: "https://www.googleapis.com/oauth2/v3/certs" },
  { provider: "Okta (dev-18545162)", url: "https://dev-18545162.okta.com/oauth2/default/v1/keys" },
  { provider: "Okta (Crunchyroll Partner Stg)", url: "https://auth.stg.partner.crunchyroll.com/oauth2/v1/keys" },
  { provider: "Okta (Crunchyroll Main)", url: "https://crunchyroll.okta.com/oauth2/v1/keys" },
  { provider: "Auth0", url: "https://example.auth0.com/.well-known/jwks.json" },
  { provider: "Microsoft", url: "https://login.microsoftonline.com/common/discovery/v2.0/keys" },
  { provider: "AWS Cognito (us-east-1)", url: "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_Wt2sA2K9e/.well-known/jwks.json" },
  { provider: "AWS Cognito (us-west-2)", url: "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_rurUnzXRE/.well-known/jwks.json" },
];

async function measureLatency(endpointUrl, timeout = 10000) {
  const start = performance.now();
  // Make the GET request using node-fetch with the custom HTTPS agent
  await fetch(endpointUrl, { agent: httpsAgent, timeout });
  const end = performance.now();
  return (end - start) / 1000; // return latency in seconds
}

async function main(iterations, outputCSV) {
  // Write CSV header
  fs.writeFileSync(outputCSV, 'provider,endpoint,iteration,latency_seconds, style\n');

  for (const endpoint of endpoints) {
    for (let i = 1; i <= iterations; i++) {
      try {
        const latency = await measureLatency(endpoint.url);
        fs.appendFileSync(outputCSV, `${endpoint.provider},${endpoint.url},${i},${latency},"js-node-fetch"\n`);
        console.log(`${endpoint.provider} (iteration ${i}): ${latency.toFixed(4)} sec`);
      } catch (error) {
        const errMsg = error.message || error;
        fs.appendFileSync(outputCSV, `${endpoint.provider},${endpoint.url},${i},"error: ${errMsg}"\n`);
        console.log(`Error for ${endpoint.provider} (iteration ${i}): ${errMsg}`);
      }
    }
  }
  console.log(`\nLatency measurements completed. Results saved in '${outputCSV}'.`);
}

main(args.iterations, args.output);
