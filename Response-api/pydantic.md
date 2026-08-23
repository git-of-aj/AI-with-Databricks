# Pydantic: The 80/20 You Should Learn

Yes. If your goal is real-world Python/backend work, you don't need to learn every Pydantic feature. You need a small set of concepts really well.

Think of Pydantic as:

> Python type hints + validation + conversion + serialization

For example, instead of manually checking incoming data:

```python
data = {
    "name": "John",
    "age": "25"
}
```

you define what you expect:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

Then:

```python
user = User(**data)

print(user.name)  **John
print(user.age)   # 25
```

**dantic validates the data and can**onvert compatible input types.

-**

## 1. BaseModel (Most Important**oncept)

Almost everything starts**ere.

```python
from pydantic imp**t BaseModel

class User(BaseModel**
    name: str
    age: int
    e**il: str

user = User(
    name="J**n",
    age=25,
    email="john@e**mple.com"
)
```

Think:

```text
**seModel
   ↓
Defines the shape of**our data
   ↓
Validates incoming **ta
   ↓
Gives you a Python object**``

You'll use this constantly.

**-

## 2. Required vs Optional Fie**s

```python
class User(BaseModel**
    name: str
    age: int
```

**th fields are required.

If you w**t an optional value:

```python
c**ss User(BaseModel):
    name: str**   age: int | None = None
```

No**this is valid:

```python
user = **er(name="John")
```

And:

```pyt**n
user.age
```

returns:

```pyth**
None
```

### Modern Syntax

Pre**rred:

```python
str | None
```

**der syntax:

```python
Optional[s**]
```

Both work, but `str | None**is the modern style.

---

## 3. **fault Values

```python
class Use**BaseModel):
    name: str
    act**e: bool = True
    age: int | Non**= None
```

```python
user = User**ame="John")
```

Produces:

```py**on
{
    "name": "John",
    "act**e": True,
    "age": None
}
```

**-

## 4. Validation

One of Pydan**c's biggest purposes.

```python
**ass User(BaseModel):
    name: st**    age: int
```

Then:

```pytho**User(name="John", age="hello")
``**
raises a validation error.

No n**d to write:

```python
if not isi**tance(age, int):
    ...
```

Pyd**tic handles it.

---

## 5. Autom**ic Type Conversion

```python
use**= User(
    name="John",
    age=**5"
)
```

Pydantic may convert `"**"` into:

```python
25
```

```py**on
print(user.age)
print(type(use**age))
```

Output:

```python
25
**lass 'int'>
```

Pydantic can con**rt compatible inputs, but it won'**convert everything.

---

## 6. N**ted Models

Input data:

```json
**  "name": "John",
  "address": {
**  "city": "Dubai",
    "country":**UAE"
  }
}
```

Model it like thi**

```python
class Address(BaseMod**):
    city: str
    country: str**class User(BaseModel):
    name: **r
    address: Address
```

```py**on
user = User(
    name="John",
**  address={
        "city": "Duba**,
        "country": "UAE"
    }
**```

Now:

```python
user.address**ity
```

works.

Very useful for:**- APIs
- Databases
- JSON
- Confi**ration
- FastAPI
- AI/LLM respons**

---

## 7. Lists of Models

```**thon
class Product(BaseModel):
  **name: str
    price: float

class**rder(BaseModel):
    products: li**[Product]
```

```python
order = **der(
    products=[
        {"nam**: "Laptop", "price": 1000},
     ** {"name": "Mouse", "price": 50}
 ** ]
)
```

Pydantic validates ever**product.

Examples:

```python
pr**ucts: list[str]
prices: list[floa**
users: list[User]
```

---

## 8**Field()

Used for constraints and**etadata.

```python
from pydantic**mport BaseModel, Field

class Use**BaseModel):
    name: str = Field**in_length=2)
    age: int = Field**t=0)
```

Now:

```python
age = 0**``

is invalid.

String constrain**:

```python
Field(
    min_lengt**2,
    max_length=100
)
```

Nume**c constraints:

```python
Field(
**  gt=0,
    lt=150
)
```

Meaning**
```text
gt = greater than
ge = g**ater than or equal
lt = less than**e = less than or equal
```

---

** 9. EmailStr and Other Special Ty**s

```python
from pydantic import**aseModel, EmailStr

class User(Ba**Model):
    name: str
    email: **ailStr
```

Pydantic validates em**l format automatically.

Other us**ul types:

```python
from pydanti**import HttpUrl

class Website(Bas**odel):
    url: HttpUrl
```

Much**leaner than writing your own vali**tors.

---

## 10. model_dump()

**ry important.

```python
class Us**(BaseModel):
    name: str
    ag** int

user = User(name="John", ag**25)
```

```python
user.model_dum**)
```

Result:

```python
{
    "**me": "John",
    "age": 25
}
```
**ental model:

```text
Pydantic Mo**l
       ↓
 model_dump()
       ↓**   dict
```

---

## 11. model_du**_json()

Convert a model into JSO**

```python
user.model_dump_json(**```

Result:

```json
{"name":"Jo**","age":25}
```

Pretty JSON:

``**ython
user.model_dump_json(indent**)
```

Output:

```json
{
  "name** "John",
  "age": 25
}
```

Remem**r:

```text
model_dump()       → **ct
model_dump_json()  → JSON stri**
```

---

## 12. model_validate(**
Converts external data into a Py**ntic model.

```python
data = {
 ** "name": "John",
    "age": 25
}
**`

```python
user = User.model_va**date(data)
```

Mental model:

``**ext
dict
   ↓
model_validate()
  **
Pydantic Model
```

Opposite dir**tion:

```text
Pydantic Model
   **  ↓
model_dump()
       ↓
dict
``**
Remember this pair:

```python
U**r.model_validate(data)
user.model**ump()
```

---

## 13. JSON → Pyd**tic Model

If you receive JSON te**:

```python
json_data = '{"name"**"John", "age": 25}'
```

```pytho**user = User.model_validate_json(j**n_data)
```

Mental model:

```te**
JSON
 ↓
model_validate_json()
 ↓**ydantic Model
```

Reverse direct**n:

```text
Pydantic Model
 ↓
mod**_dump_json()
 ↓
JSON
```

Very us**ul for APIs.

---

## 14. @field_**lidator

Custom validation for a **ngle field.

```python
from pydan**c import BaseModel, field_validat**

class User(BaseModel):
    user**me: str

    @field_validator("us**name")
    @classmethod
    def v**idate_username(cls, value):
     ** if " " in value:
            rai** ValueError(
                "Use**ame cannot contain spaces"
      **    )
        return value
```

T**s fails:

```python
User(username**john doe")
```

Think:

```text
f**ld_validator
       ↓
    One fie**
```

---

## 15. @model_validato**
Validation involving multiple fi**ds.

```python
from pydantic impo** BaseModel, model_validator

clas**PasswordChange(BaseModel):
    pa**word: str
    confirm_password: s**

    @model_validator(mode="afte**)
    def passwords_match(self):
**      if self.password != self.co**irm_password:
            raise V**ueError(
                "Passwor** do not match"
            )

   **   return self
```

Think:

```te**
field_validator
      ↓
   One f**ld

model_validator
      ↓
 Mult**le fields
```

---

## 16. Enum

**strict allowed values.

```python**rom enum import Enum
from pydanti**import BaseModel

class Role(str,**num):
    ADMIN = "admin"
    USE**= "user"
    GUEST = "guest"

cla** User(BaseModel):
    name: str
 ** role: Role
```

Allowed values:
**``text
admin
user
guest
```

Usef** for API requests and business ru**s.

---

## 17. Aliases

External**SON and Python names don't always**atch.

API sends:

```json
{
  "f**stName": "John"
}
```

But your P**hon code wants:

```python
first_**me
```

```python
from pydantic i**ort BaseModel, Field

class User(**seModel):
    first_name: str = F**ld(alias="firstName")
```

Now:

**`python
user.first_name
```

work**while accepting:

```json
{
  "fi**tName": "John"
}
```

---

## 18.**onfigDict

Configuration in Pydan**c v2.

```python
from pydantic im**rt BaseModel, ConfigDict

class U**r(BaseModel):
    model_config = **nfigDict(
        extra="forbid"
**  )

    name: str
    age: int
`**

Now this fails:

```python
User**    name="John",
    age=25,
    **mething="hello"
)
```

Because `s**ething` isn't defined.

Common op**ons you'll encounter:

```text
ex**a
frozen
validate_assignment
popu**te_by_name
from_attributes
```

D**'t memorize them all yet.

---

#**19. ValidationError

```python
fr** pydantic import ValidationError
**ry:
    user = User(
        name**John",
        age="hello"
    )
**cept ValidationError as e:
    pr**t(e)
```

Pydantic provides detai**d information about validation fa**ures.

Frameworks like FastAPI of**n handle these errors automatical**.

---

## 20. JSON Schema

Generate schema metadata from your model:

```python
User.model_json_schema()
```

Useful for:

- APIs
- OpenAPI
- FastAPI
- Documentation
- AI structured outputs

Example model:

```python
class User(BaseModel):
    name: str
    age: int
```

Schema conceptually describes:

```text
name → string
age  → integer
```

---

# Daily-Use Cheat Sheet

| Goal | Pydantic |
|--------|--------|
| Create model | `class X(BaseModel)` |
| Define field | `name: str` |
| Optional field | `name: str \| None = None` |
| Default value | `active: bool = True` |
| Constraints | `Field(...)` |
| Nested model | `address: Address` |
| List of models | `users: list[User]` |
| Validate one field | `@field_validator` |
| Validate multiple fields | `@model_validator` |
| Dict → model | `Model.model_validate(data)` |
| JSON → model | `Model.model_validate_json(json)` |
| Model → dict | `model.model_dump()` |
| Model → JSON | `model.model_dump_json()` |
| JSON schema | `model.model_json_schema()` |
| Validation error handling | `ValidationError` |
| Configuration | `ConfigDict` |
| Restricted values | `Enum` |

---

# Mental Model to Remember

```text
                 PYDANTIC
                    │
        ┌───────────┴───────────┐
        │                       │
   INPUT DATA               PYTHON MODEL
        │                       │
        │                       │
        ▼                       ▼
model_validate()          model_dump()
        │                       │
        ▼                       ▼
 Pydantic Model              dict
        │
        │
        ▼
model_dump_json()  → JSON
```

For JSON input:

```text
JSON
 │
 ▼
model_validate_json()
 │
 ▼
Pydantic Model
```

---

# Learning Order

Don't try to learn 50 features at once.

Learn in this order:

1. BaseModel
2. Fields + type hints
3. Required vs optional fields
4. Defaults
5. Nested models
6. Lists/dicts of models
7. Field()
8. model_dump()
9. model_validate()
10. model_dump_json()
11. model_validate_json()
12. ValidationError
13. field_validator
14. model_validator
15. Enum
16. Aliases
17. ConfigDict
18. JSON Schema

---

# Core Flow

Don't learn Pydantic as a collection of methods.

Learn the flow:

```text
External/Untrusted Data
           ↓
     Pydantic validates
           ↓
     Typed Python model
           ↓
 Business/Application Logic
           ↓
      model_dump()
           ↓
           dict
```

Or:

```text
JSON
 ↓
model_validate_json()
 ↓
Pydantic Model
 ↓
model_dump_json()
 ↓
JSON
```

Once this mental model clicks, FastAPI, API clients, configuration management, and structured LLM outputs become much easier to understand.

---

# What is `model_dump_json()`?

Given:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="John", age=25)
```

Convert to JSON:

```python
user.model_dump_json()
```

Output:

```json
{"name":"John","age":25}
```

Simple summary:

```text
model_dump()       → Python dictionary
model_dump_json()  → JSON string
```

Example:

```python
user.model_dump()
```

Returns:

```python
{
    "name": "John",
    "age": 25
}
```

While:

```python
user.model_dump_json()
```

Returns:

```python
'{"name":"John","age":25}'
```

Notice the second is a string.

---

# What Does `indent=2` Mean?

```python
user.model_dump_json(indent=2)
```

Without indentation:

```json
{"name":"John","age":25}
```

With `indent=2`:

```json
{
  "name": "John",
  "age": 25
}
```

The `2` means:

> Use 2 spaces for each indentation level.

You could also use:

```python
user.model_dump_json(indent=4)
```

Output:

```json
{
    "name": "John",
    "age": 25
}
```

---

# Why Use `indent=2`?

For readability and debugging.

```python
print(user.model_dump_json(indent=2))
```

Output:

```json
{
  "name": "John",
  "age": 25
}
```

Much easier for humans to read.

When sending JSON to APIs, you typically don't need indentation because compact JSON is smaller:

```json
{"name":"John","age":25}
```

---

# Quick Summary

```text
model_dump()                  → dict
model_dump_json()             → JSON string
model_dump_json(indent=2)     → Pretty JSON string
```

Important distinction:

```python
data = user.model_dump()
```

`data` is a Python dictionary.

```python
data = user.model_dump_json(indent=2)
```

`data` is a string containing JSON.

This distinction is important when working with APIs, databases, files, and message queues.