#!/usr/bin/env python3
"""
One-shot Railway deployment script.

Usage:
  RAILWAY_TOKEN=xxx FIRECRAWL_API_KEY=yyy APIFY_API_TOKEN=zzz python deploy_railway.py

Or set the variables inline:
  python deploy_railway.py
  (it will prompt for missing values)
"""
import json
import os
import sys
import urllib.request
import urllib.error

API = "https://backboard.railway.app/graphql/v2"
GITHUB_REPO = "choujame/mcp-server"
PROJECT_NAME = "mcp-server"


def gql(token, query, variables=None):
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            if "errors" in result:
                raise RuntimeError(result["errors"])
            return result["data"]
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}")


def prompt(name, env_key, secret=False):
    val = os.environ.get(env_key, "")
    if val:
        return val
    import getpass
    fn = getpass.getpass if secret else input
    val = fn(f"{name}: ").strip()
    if not val:
        print(f"[skip] {name} not provided — you can add it later in Railway dashboard")
    return val


def main():
    print("=== Railway MCP Server Deployment ===\n")

    token = prompt("Railway API Token", "RAILWAY_TOKEN", secret=True)
    if not token:
        sys.exit("Railway token is required.")

    firecrawl_key = prompt("FIRECRAWL_API_KEY", "FIRECRAWL_API_KEY", secret=True)
    apify_token = prompt("APIFY_API_TOKEN", "APIFY_API_TOKEN", secret=True)

    # 1. Verify token
    print("\n[1/5] Verifying token...")
    me = gql(token, "query { me { id name email } }")["me"]
    print(f"      Logged in as: {me['name']} ({me['email']})")

    # 2. Create project
    print(f"[2/5] Creating project '{PROJECT_NAME}'...")
    project = gql(token, """
        mutation($input: ProjectCreateInput!) {
          projectCreate(input: $input) { id name defaultEnvironment { id } }
        }
    """, {"input": {"name": PROJECT_NAME}})["projectCreate"]
    project_id = project["id"]
    env_id = project["defaultEnvironment"]["id"]
    print(f"      Project ID: {project_id}")

    # 3. Create service from GitHub
    print(f"[3/5] Connecting GitHub repo '{GITHUB_REPO}'...")
    service = gql(token, """
        mutation($input: ServiceCreateInput!) {
          serviceCreate(input: $input) { id name }
        }
    """, {"input": {
        "projectId": project_id,
        "name": "mcp-server",
        "source": {"repo": GITHUB_REPO},
    }})["serviceCreate"]
    service_id = service["id"]
    print(f"      Service ID: {service_id}")

    # 4. Set environment variables
    print("[4/5] Setting environment variables...")
    env_vars = {"MCP_TRANSPORT": "sse"}
    if firecrawl_key:
        env_vars["FIRECRAWL_API_KEY"] = firecrawl_key
    if apify_token:
        env_vars["APIFY_API_TOKEN"] = apify_token

    for name, value in env_vars.items():
        gql(token, """
            mutation($input: VariableUpsertInput!) {
              variableUpsert(input: $input)
            }
        """, {"input": {
            "projectId": project_id,
            "serviceId": service_id,
            "environmentId": env_id,
            "name": name,
            "value": value,
        }})
        print(f"      {name} ✓")

    # 5. Generate domain
    print("[5/5] Generating public domain...")
    domain_result = gql(token, """
        mutation($serviceId: String!, $environmentId: String!) {
          serviceDomainCreate(serviceId: $serviceId, environmentId: $environmentId) {
            domain
          }
        }
    """, {"serviceId": service_id, "environmentId": env_id})
    domain = domain_result["serviceDomainCreate"]["domain"]

    print(f"\n{'='*45}")
    print(f"  Deployment triggered!")
    print(f"  MCP Server URL:")
    print(f"  https://{domain}/sse")
    print(f"{'='*45}")
    print(f"\nOnce deployment finishes (~1 min), run:")
    print(f"  claude mcp add --scope user --transport sse my-scraper https://{domain}/sse")


if __name__ == "__main__":
    main()
