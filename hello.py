import requests
import time
import csv
import argparse

# List of endpoints with provider names
endpoints = [
    {"provider": "Google", "url": "https://www.googleapis.com/oauth2/v3/certs"},
    {"provider": "Okta (default)", "url": "https://dev-123456.okta.com/oauth2/default/v1/keys"},
    {"provider": "Okta (Crunchyroll)", "url": "https://auth.stg.partner.crunchyroll.com/oauth2/v1/keys"},
    {"provider": "Auth0", "url": "https://example.auth0.com/.well-known/jwks.json"},
    {"provider": "Microsoft", "url": "https://login.microsoftonline.com/common/discovery/v2.0/keys"},
    {"provider": "AWS Cognito", "url": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_ExaMPle/.well-known/jwks.json"},
]

def measure_latency(endpoint_url, timeout=10):
    """
    Performs a GET request to the given URL and returns the elapsed time in seconds.
    """
    start = time.time()
    response = requests.get(endpoint_url, timeout=timeout)
    # Optionally, you can check response.status_code here.
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
                    latency = measure_latency(endpoint["url"])
                    writer.writerow([endpoint["provider"], endpoint["url"], i, latency])
                    print(f'{endpoint["provider"]} (iteration {i}): {latency:.4f} sec')
                except Exception as e:
                    writer.writerow([endpoint["provider"], endpoint["url"], i, f"error: {e}"])
                    print(f'Error for {endpoint["provider"]} (iteration {i}): {e}')

    print(f"\nLatency measurements completed. Results saved in '{output_csv}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure latencies of OAuth provider JWKS endpoints.")
    parser.add_argument("-n", "--iterations", type=int, default=20, help="Number of iterations per endpoint (default: 5)")
    parser.add_argument("-o", "--output", type=str, default="endpoint_latencies.csv", help="Output CSV file (default: endpoint_latencies.csv)")
    
    args = parser.parse_args()
    main(args.iterations, args.output)

