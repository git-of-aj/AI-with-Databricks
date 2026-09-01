## Databricks Service principal
https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/service-principals

The Azure Databricks host.

- For account operations, specify https://accounts.azuredatabricks.net.
- For workspace operations, Databricks recommends specifying the per-workspace URL, for example https://adb-1234567890123456.7.azuredatabricks.net and explicitly assigning the Microsoft Entra service principal to the workspace. Alternatively, specify the Azure resource ID. This approach requires Contributor or Owner permissions on the Azure resource, or a custom role with specific Azure Databricks permissions.
Link: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/azure-sp
- Databricks recommends using DATABRICKS_HOST and explicitly assigning the Microsoft Entra service principal to the workspace. Alternatively, use DATABRICKS_AZURE_RESOURCE_ID with the Azure resource ID. This approach requires Contributor or Owner permissions on the Azure resource, or a custom role with specific Azure Databricks permissions.

## Azure-identity
- for managed identity: https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#authenticate-azure-hosted-applications

## Handle response
how do you know if its json or dictionary ?

Good question. The key is that JSON and Python dictionaries are not the same thing.

1. response.json() returns a Python object

With the requests library:

data = response.json()

The .json() method reads the JSON response and converts it into Python data structures.

For your response, the conversion is roughly:

JSON                         Python
------------------------------------------------
{ }                          dict
[ ]                          list
"hello"                      str
123                          int
true                         True
false                        False
null                         None

So your JSON:

### Azure Monitor Alert Beahviour 
```txt
ADF failures
   ↓
Metric = PipelineFailedRuns
   ↓
Alert condition becomes TRUE
   ↓
Alert instance = FIRED
   ↓
Action Group executes
   ↓
             ┌─────────────────────────────┐
             │ Alert remains FIRED         │
             │ while condition stays true  │
             └─────────────────────────────┘
                         ↓
                  More ADF failures
                         ↓
              NO NEW ALERT INSTANCE
                         ↓
                 NO NEW ACTION GROUP

```
- This is stateful alert behavior.

- Azure Monitor metric alerts are stateful by default. Once a metric alert fires for a particular metric time series, Azure doesn't fire another alert/action for every subsequent evaluation while the condition remains true. It waits for the condition to resolve

I can see the problem now. Your App Registration itself is probably fine. The issue is that you're searching for the scope by typing its URI, but the Action Group picker is not finding an exposed API scope that Azure Monitor can use.

Also, your screenshot reveals one important difference from your first screenshot:

Identity = User-assigned managed identity

That's okay, but it means we need to make sure that this exact user-assigned managed identity is authorized to call your Function App.

Microsoft's current documentation says Azure Function + managed identity requires the “Function App authorization (Microsoft Entra ID)” authorization on the target Function App. 
M
Microsoft Learn

Do this first — don't change the Scope box yet
1. Identify the User Assigned Managed Identity

In your screenshot, the identity says:

User-assigned m...

Click that dropdown and note the exact name of the managed identity.

Let's call it:

<AG-MANAGED-IDENTITY>


This is not your App Registration.

That's an important distinction:

App Registration
        ↓
protects your Function API

User-assigned Managed Identity
        ↓
Azure Monitor uses this identity to call the Function

2. Give that managed identity access to the Function App

Go to:

Function App → monitor-ind-78 → Access control (IAM)

Then:

Add → Add role assignment

Search for:

Function App authorization


You should find the role:

Function App authorization (Microsoft Entra ID)

This is the role Microsoft currently documents specifically for Azure Function actions using managed identity. 
M
Microsoft Learn

Select it.

Members

Choose:

Managed identity

Then:

Select members

For the managed identity type, choose:

User-assigned managed identity

Select the same identity that you selected in your Action Group.

Then:

Review + assign

3. Wait a few minutes after the role assignment

This is the propagation that actually matters.

You don't need to wait for the App Registration itself.

After the role assignment, give Azure RBAC a few minutes, then refresh the Action Group page.

4. Now check your Function App Authentication

Go to:

Function App → monitor-ind-78 → Authentication

Your Microsoft Entra provider should point to the App Registration you created.

Then look at:

Allowed token audiences

You should have:

api://89f7a986-b7e0-4cf6-814d-06de06a6603e


assuming that GUID in your screenshot is the Application/Client ID of your App Registration.

Do not enter:

api://89f7a986-b7e0-4cf6-814d-06de06a6603e/user_impersonation


as the audience.

The audience is the API identifier; the /user_impersonation portion is the scope.

5. Check Expose an API

Open:

Microsoft Entra ID → App registrations → your Function App registration → Expose an API

You should have:

Application ID URI
api://89f7a986-b7e0-4cf6-814d-06de06a6603e


And underneath:

Scope
user_impersonation


The resulting full scope is:

api://89f7a986-b7e0-4cf6-814d-06de06a6603e/user_impersonation

6. Here's the key thing about your screenshot

You're currently typing:

api://89f7a986-b7e0-4cf6-814d-06de06a6603e


into the Scope picker.

That's not the complete scope.

Try searching for:

user_impersonation


instead.

Or, if the picker supports the full value, search:

api://89f7a986-b7e0-4cf6-814d-06de06a6603e/user_impersonation

But don't manually type it and expect it to become selectable.

The important part is that Azure needs to discover the exposed API/scope. If the dropdown says:

No results were found

then the portal isn't currently discovering your API scope.

7. If it STILL says "No results"

Then I want you to check one specific thing.

Go to:

Microsoft Entra ID → App registrations → your app → Expose an API

and look at Authorized client applications.

You don't necessarily need to add anything there just because you're using managed identity, so don't randomly add your Function App or Azure Monitor.

Instead, send me a screenshot of this exact page:

App Registration → Expose an API

I want to see:

Application ID URI
-------------------
api://89f7...

Scopes defined by this API
---------------------------
user_impersonation

Authorized client applications
------------------------------
...


because from your current screenshot, the missing piece is now most likely on the API exposure/authorization side rather than propagation.

One correction to my earlier instructions

I previously told you that the Action Group Scope should simply be:

api://<CLIENT_ID>/user_impersonation


That's the logical API scope, but the portal's picker isn't a free-text field. The fact that your dropdown returns “No results were found” means we need to fix the Azure resource/API authorization relationship rather than just keep typing the URI.

And Microsoft's current documentation confirms that this managed-identity Function integration is still a preview feature, with the Function App authorization being the required authorization mechanism. 
M
Microsoft Learn

So your next action

Don't create another App Registration.

Do these two things:

Assign Function App authorization (Microsoft Entra ID) to the User Assigned Managed Identity you're using in the Action Group.
Send me the Expose an API screenshot.

I'll then tell you exactly what is missing.

M
Sources