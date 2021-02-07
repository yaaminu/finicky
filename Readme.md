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
        "version":validators.is_str(required=True, pattern=r"\d+\.\d+\.\d+"),
        "stars":validators.is_int(required=False, min=0, default=0)
    })
    
    errors, validated_repo = repo_schema.validate(data=repo)
    if errors: #validation failed
        for key in errors.keys():
            print(f"{key}: {errors[key]}")
    else:
        use_validated_data(validated_repo)
        # .. more code
```

### Schemas
A schema is a case-sensitive mapping of field names to their corresponding validators. Pyval comes with set
of predefined validators that cover most use cases but you may define custom ones if the inbuilt validators don't work 
for your use case. These validators are described in the validators section.
**Example**
```python
repo_schama = {
    "name": name_validator,
    "version": version_valdiator,  
    "stars":stars_validator
}
```

#### Validators
A validator is a function that takes a single argument and raises a `pyval.validators.ValidationException` when its 
argument is invalid or returns the input successful validation. The input may be modified before returning it. 
```python
import re
def version_validator(input:any)-> str:
    input = str(input).strip()
    if re.match(r"\A\d+\.\d+\.\d+\Z", input):
        return input
    raise ValidationException("validation failed")
```

#### Hooks
In some situations, the validity of an input may depend on complex conditions and relationship between multiple fields.
Pyval allows you to define a function that shall be invoked with the input data after all field level validation have
succeeded. This hook can then run the necessary validation returning the input on success or raising a
ValidationException on success. Example, a price data may contain all valid fields but you may want to ensure that
selling price is always greater than cost rice. Hooks are useful for these kind of checks. 

**Example Usage**
```python
def hook(price): 
    # hook will only be called if all fields have passed validation 
    if price["selling_price"] < price["cost_price"]:
        raise  ValidationException("selling price cannot be less than cost price")
    return price
```

#### Putting It All Together
```python
from pyval.schema import validate
from pyval.validators import  is_int,is_float, ValidationException

data = {"product_id":2, "cost_price":1.2, "selling_price":1.8}
schema = {
    "product_id":is_int(min=1, required=True),
    "cost_price":is_float(min=0.1, round_to=2, required=True), 
    "selling_price":is_float(min=0.1, round_to=2, required=True)
}
errors, validated_price = validate(schema=schema, data=data, hook=price_hook)
if errors:
   print(f"errors occurred {errors}")
else:
   use_price_data(validated_price)
```


### Built-in Validators
Pyval comes with predefined validators that you can use right away. They are essentially factory functions that returns
another function that take in one argument (the data to be validated) and return the validated data on success or raise
`ValidationException` on failure. 

#### is_str 
A factory function that returns a validator for validating texts.
 
It takes in the following arguments:
1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value. 
3. `min_len`: The minimum length allowed, defaults to 0 
4. `max_len`: The maximum length allowed, defaults to `None`
5. `pattern`: An optional regular expression to which the input must match. Pattern matching is accomplished with 
              the standard python `re` package.  Be careful when using this on untrusted input as you may expose
              yourself to regular expression denial attacks. 

#### is_int
A factory function that returns a validator for validating integers.

It takes in the following arguments:
1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value.
3. `min`: The minimum value allowed, defaults to 0 
4. `max`: The maximum value allowed, defaults to `None`


#### is_float
A factory function that returns a validator for validating floating point numbers. 

It takes in the following arguments:
1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value.
3. `min`: The minimum value allowed, defaults to 0 
4. `max`: The maximum value allowed, defaults to `None`
5. `round_to`: The number of decimal places to which the input must be rounded to. 

#### is_date
A factory function that returns a validator for validating dates.
The date validator can work directly with `datetime.datetime` objects or date strings. 

It takes in the following arguments:
1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value. 
3. `min`: The minimum date allowed, defaults to `None` 
4. `max`: The maximum date allowed, defaults to `None`
5. `format`: The format in which date is formatted. This is only used when the input is a string literal. It's 
             important to note that python's date formatter is not forgiving so all fields specified in 
             the format must be present in the input string. Example the format "%Y-%m-%d %H:%M" can't work with
             "2020-12-12 12:30:20" because the format doesn't include a millisecond field

#### is_list
A validator factory that returns a function for validating lists. By default, all entries must pass the validation else
the field would be considered invalid. This can be overridden by setting `all` to `false` (see below). 

It takes in the following arguments:
1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value.
3. `min_len`: The minimum number of entries allowed, defaults to 0
4. `max_len`: The maximum number of entries, defaults to `None`
5. `validator`: A validator for validating each entry in the list. 
6. `all`: When `True`, all fields must pass validation for this list to be considered valid. When `False` at least one
           entry must pass validation for this list to be considered valid. Only entries that pass validation shall 
           be returned. 

#### is_dict
A validator factory that returns a function for validating python dictionaries.

It takes in the following arguments:
1. `required`: `bool` - `True` when the field is required, `False` otherwise. `True` by default
2. `default`: The default value.
5. `schema`: A schema for validating this dictionary, same as the schema described above. 

   
#### custom validators
In some situations where the built-in validators don't work for you, pyval allows you to define your own validator. 
Validators are essentially functions that take in a single input and return the newly validated input on success or 
raise a `pyval.validators.ValidationException` for invalid input. A simple example maybe checking if a field is a valid
ip-address. 
```python
import re
from pyval.validators import ValidationException, is_str
from pyval import validate

def is_ipv4_address(input):
    if not input:
        raise ValidationException("this field is required")
    input = str(input).strip()
    if not re.match(r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z", input):
        raise ValidationException("This field must be an ipv4 address")
    parts = input.split(".") 
    assert len(parts) == 4 # this should produce 4 parts else the regex test should have failed
    if any(int(part) > 255 for part in parts):
        raise ValidationException("This field must be a valid ipv4 address") 
    return input

my_schema = {
    "sender_ip":is_ipv4_address,
    "message":is_str(min_len=1, max_len=200) 
}

err, val = validate(schema=my_schema, data={"sender_ip":"127.0.0.1", "message":"PING"})
## code continues
```  


### Handling Errors 
All validation errors are returned in a list with the field name prepended to the error message. An input is considered
invalid if this list is not empty. 

#### contributing
Spot a bug? feature request? want to improve documentation? Kindly open an issue or make a pull request, your feedback 
is welcome.


