In simple English, this flow means:

Browser → Microsoft Entra ID

The user opens the web application and signs in.
Microsoft Entra ID verifies the user and issues a security token.

Browser → FastAPI (Bearer Token)

The browser sends that token to your FastAPI backend with each request.
This token proves who the user is.

FastAPI → OBO (On-Behalf-Of) Token Exchange

FastAPI needs to call another Microsoft service on behalf of the user.
Instead of asking the user to log in again, FastAPI sends the user's token to Microsoft Entra ID.
Entra ID exchanges it for a new token that is valid for the downstream service.
This is called the On-Behalf-Of (OBO) flow.

FastAPI → Microsoft Foundry

FastAPI uses the new downstream token to access Microsoft Foundry as the signed-in user.

Microsoft Foundry → Agent Framework

Foundry forwards the request to an AI agent.

Agent Framework → MCP

The agent uses MCP (Model Context Protocol) tools or services to perform actions.

Approval Request

If a sensitive action needs user approval (for example, sending an email or modifying data), the agent pauses and requests approval.

Browser Approval

The approval request is shown to the user in the browser.
The user approves or rejects it.

Agent Continues

If approved, the agent resumes and completes the task.
Why use OBO?

Without OBO:

User signs in to Browser.
FastAPI wants to call Microsoft Foundry.
User would have to sign in again.

With OBO:

User signs in once.
FastAPI securely obtains a downstream token on behalf of the user.
The user's identity and permissions are preserved across services.
No additional login prompt is required.

A simple analogy:

You (the user) give a receptionist (FastAPI) permission to act for you. The receptionist goes to another department (Microsoft Foundry) and gets access using your authorization, without bringing you there to sign in again. That's the On-Behalf-Of (OBO) flow.