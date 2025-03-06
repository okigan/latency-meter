import requests
import time
import csv
import argparse

# List of endpoints with provider names
endpoints = [
    {"provider": "Crunchyroll", "url": "https://prd.partner.crunchyroll.com/api/core/healthcheck"},
    {"provider": "Google", "url": "https://www.googleapis.com/oauth2/v3/certs"},
    {"provider": "Okta (dev-123456)", "url": "https://dev-123456.okta.com/oauth2/default/v1/keys"},
    {"provider": "Okta (Crunchyroll Partner Stg)", "url": "https://auth.stg.partner.crunchyroll.com/oauth2/v1/keys"},
    {"provider": "Okta (Crunchyroll Main)", "url": "https://crunchyroll.okta.com/oauth2/v1/keys"},
    {"provider": "Auth0", "url": "https://example.auth0.com/.well-known/jwks.json"},
    {"provider": "Microsoft", "url": "https://login.microsoftonline.com/common/discovery/v2.0/keys"},
    {"provider": "AWS Cognito (us-east-1)", "url": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_Wt2sA2K9e/.well-known/jwks.json"},
    {"provider": "AWS Cognito (us-west-2)", "url": "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_rurUnzXRE/.well-known/jwks.json"},

]

session = requests.Session()

def measure_latency(session, endpoint_url, timeout=10):
    start = time.time()
    response = session.get(endpoint_url, timeout=timeout)
    end = time.time()
    return end - start

def main(iterations, output_csv):
    # Open CSV file for writing the results
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["provider", "endpoint", "iteration", "latency_seconds"])
        
        # Iterate over each endpoint and repeat the measurement
        for endpoint in endpoints:
            for i in range(1, iterations + 1):
                try:
                    latency = measure_latency(session, endpoint["url"])
                    writer.writerow([endpoint["provider"], endpoint["url"], i, latency])
                    print(f'{endpoint["provider"]} (iteration {i}): {latency:.4f} sec')
                except Exception as e:
                    writer.writerow([endpoint["provider"], endpoint["url"], i, f"error: {e}"])
                    print(f'Error for {endpoint["provider"]} (iteration {i}): {e}')

    print(f"\nLatency measurements completed. Results saved in '{output_csv}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure latencies of OAuth provider JWKS endpoints.")
    parser.add_argument("-n", "--iterations", type=int, default=40, help="Number of iterations per endpoint (default: 5)")
    parser.add_argument("-o", "--output", type=str, default="endpoint_latencies.csv", help="Output CSV file (default: endpoint_latencies.csv)")
    
    args = parser.parse_args()
    main(args.iterations, args.output)

