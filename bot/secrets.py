
def load(name: str) -> str:
    value = ""
    with open(f"/var/openfaas/secrets/{name}") as f:
        value = f.read().strip()

    return value


slack_signing_secret = load("slack-signing-secret")
slack_api_token = load("slack-api-token")
