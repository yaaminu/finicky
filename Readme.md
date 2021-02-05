# Pyval - Easy data validation 

## Motivation 
There are many libraries available for validating data in python such as pydantic, volouptous, validino, jsonvalidator,
but they all surprisingly require too much boilerplate and code ceremony. The goal of this library is to provide an
easier to use alternative. 


## Getting Started

```python
    from pyval import Schema, validators

    repo = {"name":"Pyval", "version":"0.0.1", "stars":"2000"} 
    repo_schema = Schema({
        "name":validators.is_str(min_len=3, max_len=8, required=True),
        "version":validators.is_str(required=True, pattern=r"\d+\\.\d+\\.\d+"),
        "stars":validators.is_int(required=False, min=0, default=0)
    })
    
    errors, validated_repo = repo_schema.validate(data=repo)
    if errors: #validation failed
        for field, msg in errors:
            print(field, msg)
    else:
        use_validated_data(validated_repo)
        # .. more code
```

### Schemas
Schemas is a case-sensitive mapping of field names to their corresponding validators. This library comes with standard
predifined valdators that can be used right away. Pyval comes with set of predefined validators that cover most use
cases but you may define custom ones if the inbuilt validator doesnt work for your case. These validators are described
in the vadiators section.

A validator is a function that when invoked raises a `pyval.validators.ValidationException` when validation fails and 
returns the newly validated data on success. 

#### Hooks
In some situations, the validity of an input may depend on complex conditions and relationship between multiple fields.
Pyval allows you to define a function that shall be invoked with the input data after all field level validation have
succeeded. Example, a price data may contain all valid fields but you may want to ensure that selling price is always
greater than cost rice. Hooks are useful for these kind of checks. 

**Example Usage**
```python
from pyval.schema import validate
from pyval.validators import  is_int,is_float, ValidationException

data = {"product_id":2, "cost_price":1.2, "selling_price":1.8}
schema = {
    "product_id":is_int(min=1, required=True),
    "cost_price":is_float(min=0.1, round_to=2, required=True), 
    "selling_price":is_float(min=0.1, round_to=2, required=True)
}

def hook(price): 
    # hook will only be called if all fields have passed validation 
    if price["selling_price"] < price["cost_price"]:
        raise  ValidationException("selling price cannot be less than cost price")
    return price

errors, validated_price = validate(schema=schema, data=data, hook=hook)
if errors:
   print(f"errors occurred {errors}")
else:
   use_price_data(validated_price)
```

### Validators
Validators do all the heavy lifting and Pyval comes with predefined valdiators that you can use right away.
They are essentially functions that take in one argument (the data to be validated) and return the validated data on
success or raise Validation Exception on failure. 

#### is_str 
A factory function that returns a validator for strings. It takes in the following arguments

1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value. Only allowed for non-required fields. 
3. `min_len`: The minimum length allowed, default to 0 
4. `max_len`: The maximum length allowed, default to 0
5. `pattern`: An optional regular expression to which the input must match. Pattern matching is accomplished with 
              the standard python `re` package.  Be careful when using this on untrusted input as you may expose
              yourself to regular expression denial attacks. 

#### is_int

#### is_float

#### is_date

#### is_list

#### is_dict

#### custom validators

### Handling Errors 


#### contribution

