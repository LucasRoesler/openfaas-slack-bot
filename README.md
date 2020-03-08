
faas-cli new bot --lang=pyslack

faas-cli secret create slack-api-token --from-literal=xoxb-921547957923-933041549141-J0i1Nt9ZLBoL6BCEpXoGEQrK
faas-cli secret create slack-signing-secret --from-literal=7bd05b1bca10d191f69de20866c4c144

# now write your handler
faas-cli up
