Yes—but I would not make /GET /resourceId the authorization mechanism.

The key design principle is:

The API should determine what a team is allowed to see from the authenticated identity, not trust the client to tell you which resources it owns.

For your case, I’d recommend a team → resource ownership mapping + server-side filtering.

Recommended design

Suppose you have:

Team-A
  ├── /subscriptions/.../resourceGroups/ADF/.../factories/ADF-98
  ├── /subscriptions/.../resourceGroups/ADF/.../factories/ADF-99

Team-B
  ├── /subscriptions/.../resourceGroups/ADF/.../factories/ADF-20
  └── /subscriptions/.../resourceGroups/ADF/.../factories/ADF-21


Your database could have something like:

teams
-----
id
name

resources
---------
id
resource_id
team_id


And your alerts table:

alerts
------
id
resource_id
alert_name
severity
timestamp
status
...


Then your API does:

Authenticated user
       ↓
Determine team(s)
       ↓
Determine resources owned by team
       ↓
Query alerts WHERE resource_id IN (owned resources)
       ↓
Return alerts


So Team-A calling:

GET /alerts


automatically gets only:

ADF-98
ADF-99


It doesn't need to specify the resource ID at all.

Why I prefer this over /GET /resourceId

You could technically expose:

GET /resources/{resource_id}/alerts


but the important part is that this endpoint must still perform authorization.

For example:

GET /resources/ADF-98/alerts


should not mean:

"Give me alerts for ADF-98."

It should mean:

"If the authenticated caller is authorized to access ADF-98, give them its alerts."

So internally:

@app.get("/resources/{resource_id}/alerts")
async def get_alerts(resource_id: str, user=Depends(get_current_user)):
    if not user_can_access_resource(user, resource_id):
        raise HTTPException(status_code=403)

    return get_alerts_for_resource(resource_id)


The resource_id is a filter, not an authorization credential.

That's an important distinction.

I would actually expose two endpoints
1. Team's alerts
GET /alerts


This is the primary endpoint.

Team-A:

GET /alerts


returns only Team-A's alerts.

You can support normal filters:

GET /alerts?severity=Critical
GET /alerts?status=Fired
GET /alerts?from=2026-08-01&to=2026-08-30


But never accept team_id from the client as the authorization mechanism.

For example, avoid:

GET /alerts?team_id=team-b


and then trusting that value.

The team should come from the authenticated identity/token.

2. Alerts for one resource
GET /resources/{resource_id}/alerts


This is useful when the frontend/user wants to drill into a particular resource.

For example:

GET /resources/ADF-98/alerts


Your authorization layer checks:

Does caller's team own ADF-98?
        │
       YES → return alerts
        │
       NO → 403


This gives you both:

GET /alerts


and:

GET /resources/{resource_id}/alerts


without duplicating your authorization logic.

The important part: don't hard-code teams in FastAPI

I would not do this:

TEAM_A_RESOURCES = [
    "ADF-98",
    "ADF-99",
]

TEAM_B_RESOURCES = [
    "ADF-20",
]


It works initially, but becomes painful when resources change.

Instead, put ownership in a database or configuration store.

For example:

resource_ownership
------------------
resource_id                              team_id
/subscriptions/.../factories/ADF-98     team-a
/subscriptions/.../factories/ADF-99     team-a
/subscriptions/.../factories/ADF-20     team-b


Then changing ownership becomes:

UPDATE resource_ownership
SET team_id = 'team-b'
WHERE resource_id = '...ADF-98';


rather than deploying FastAPI again.

Even better if you're already using Azure

If your teams correspond to Azure Entra ID groups, I'd strongly consider making the Entra group the source of identity.

For example:

Azure Entra ID

Team-A group
    ↓
team-a

Team-B group
    ↓
team-b


Your JWT might contain group/role information.

Then:

User
 ↓
Entra ID authentication
 ↓
Team-A group
 ↓
FastAPI authorization
 ↓
resource_ownership
 ↓
allowed resources


This gives you a very clean separation:

Entra ID
    = WHO are you?

Database / policy
    = WHAT resources does your team own?

FastAPI
    = Enforce the policy


That's much stronger than having the frontend send something like:

{
    "team": "Team-A"
}


because the client can simply change that to:

{
    "team": "Team-B"
}


if you trust request parameters.

One particularly good model

I'd use RBAC + resource-level authorization.

Think of authorization as:

User
  ↓
Role / Team
  ↓
Resource ownership
  ↓
Permission


For example:

alice@company.com
       ↓
     Team-A
       ↓
 ┌─────┴─────┐
 ↓           ↓
ADF-98      ADF-99
 ↓           ↓
 read        read


Meanwhile:

bob@company.com
       ↓
     Team-B
       ↓
     ADF-20


Bob requesting:

GET /resources/ADF-98/alerts


gets:

403 Forbidden


not ADF-98's data.

One subtle but important improvement

I'd normalize Azure resource IDs before storing/comparing them.

Azure resource IDs are effectively case-insensitive, so don't casually compare raw strings:

if requested_resource_id == stored_resource_id:


Instead normalize:

resource_id = resource_id.strip().lower()


and store the canonical/normalized form.

For example:

/subscriptions/123/resourcegroups/adf/providers/microsoft.datafactory/factories/adf-98


That prevents authorization bugs caused by casing differences.

Database query should enforce authorization

This is even better than:

alerts = get_alerts(resource_id)

if not user_can_access(resource_id):
    raise HTTPException(403)


because you don't want your application accidentally fetching data first and filtering later.

Instead make the authorization part of the query.

Conceptually:

SELECT a.*
FROM alerts a
JOIN resource_ownership ro
  ON a.resource_id = ro.resource_id
WHERE ro.team_id = :authenticated_team
  AND a.resource_id = :requested_resource;


Now the database literally cannot return an alert unless the ownership relationship exists.

For the general endpoint:

SELECT a.*
FROM alerts a
JOIN resource_ownership ro
  ON a.resource_id = ro.resource_id
WHERE ro.team_id = :authenticated_team;


That's a very strong security model.

What I would build

I'd probably structure your FastAPI like this:

/auth
    authentication

/alerts
    GET /alerts
    GET /alerts/{alert_id}

/resources
    GET /resources
    GET /resources/{resource_id}
    GET /resources/{resource_id}/alerts


But the authorization is centralized:

get_current_user()
        ↓
get_user_teams()
        ↓
get_authorized_resource_ids()
        ↓
database query


For example:

@app.get("/alerts")
async def get_alerts(
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    team_ids = user.team_ids

    return await alert_repository.get_alerts_for_teams(
        db,
        team_ids=team_ids,
    )


And:

@app.get("/resources/{resource_id}/alerts")
async def get_resource_alerts(
    resource_id: str,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not await authorization.can_access_resource(
        user,
        resource_id,
        db,
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource",
        )

    return await alert_repository.get_alerts(
        db,
        resource_id=resource_id,
    )


The critical thing is that both endpoints use the same authorization service.

My ranking of the options
Approach	Ease	Security	Scalability	Recommendation
/alerts?team=Team-A	⭐⭐⭐⭐⭐	⭐	⭐⭐	❌
/alerts?resourceId=ADF-98	⭐⭐⭐⭐⭐	⭐⭐	⭐⭐⭐	⚠️
/resources/{id}/alerts + authorization	⭐⭐⭐⭐	⭐⭐⭐⭐⭐	⭐⭐⭐⭐⭐	✅
/alerts automatically scoped to caller's team	⭐⭐⭐⭐⭐	⭐⭐⭐⭐⭐	⭐⭐⭐⭐⭐	✅ Best
Hard-coded team/resource mappings	⭐⭐⭐⭐	⭐⭐⭐	⭐	❌
Entra ID groups + DB ownership mapping	⭐⭐⭐⭐	⭐⭐⭐⭐⭐	⭐⭐⭐⭐⭐	🏆 Best overall
So my recommendation is:
Azure Monitor webhook
       ↓
     FastAPI
       ↓
     Store alert
       ↓
Azure Resource ID
       ↓
resource_ownership table
       ↓
Team ↔ Resource mapping
       ↓
Entra ID authenticated user
       ↓
GET /alerts
       ↓
ONLY team's alerts


And optionally:

GET /resources/{resource_id}/alerts


for resource-specific views.

Don't make resourceId itself responsible for access control. Make it a query/path parameter that is checked against the caller's authorization.

If you're already using Azure Entra ID, I can also sketch the exact FastAPI architecture—JWT/group claims → Team mapping → SQLAlchemy models → authorization dependency—so the ownership check is centralized rather than repeated across every endpoint.