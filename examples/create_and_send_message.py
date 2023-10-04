import os
import sys

from msgraph_outlook.graph import GraphClient
from msgraph_outlook.outlook.account import Account

# Create client with auth
client = GraphClient(
    tenant_id=os.environ.get("GRAPH_TENANT_ID"),
    client_id=os.environ.get("GRAPH_APP_ID"),
    client_secret=os.environ.get("GRAPH_CLIENT_ID"),
)

# Create account reference
acct = Account(client, user="reporting@1800radiator.com")

# New message object
msg = acct.create_message()

# Add recipient, subject, body, save draft
msg.to_recipients.add("ryancopedev@gmail.com")
msg.subject = "Test123"
msg.body = "This is a test."
msg.save_draft()

# Update body, re-save
msg.body = "This is an update test."
msg.save_draft()

# Send message
msg.send()
