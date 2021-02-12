# Yaval -  Yet Another (data) Validator

## Motivation 
There are many libraries available for validating data in python but surprisingly, they all require too much boilerplate 
and code ceremony even for simple use cases. The goal of this library is to provide an easier to use alternative.


## Getting Started

```python
from yaval import validate, is_str, is_int

repo = {"name":"Yaval", "version":"0.0.1", "stars":"2000"} 
repo_schema = {
    "name":is_str(min_len=3, max_len=8, required=True),
    "version":is_str(required=True, pattern=r"\A\d+\.\d+\.\d+\Z"),
    "stars":is_int(required=False, min=0, default=0)
}
errors, validated_repo = validate(schema=repo_schema, data=repo)
if errors: 
    # handle errors
else:
    # use validated data
```

### Schemas
A schema is a case-sensitive mapping of field names to their corresponding validators. Yaval comes with a set
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
A validator is a function that takes a single input and raises a `yaval.ValidationException` when its 
argument is invalid or returns the input upon successful validation. The input may be modified before returning it. 

**Example**
```python
import re
from yaval import ValidationException

def version_validator(input:any)-> str:
    input = str(input).strip()
    if re.match(r"\A\d+\.\d+\.\d+\Z", input):
        return input
    raise ValidationException("validation failed")
```

#### Hooks
In some situations, the validity of an input may depend on complex conditions and relationship between multiple fields.
yaval allows you to define a function that shall be invoked with the input data after all field level validations have
succeeded. This hook can then run the necessary validation returning the input on success or raise a
ValidationException on success. Example, a price data may contain valid fields but you may want to ensure that
selling price is always greater than cost rice. Hooks are useful for these kind of checks. 

**Example Usage**
```python
from yaval import ValidationException
def hook(price): 
    # hook will only be called if all fields have passed validation  
    if price["selling_price"] < price["cost_price"]:
        raise  ValidationException("selling price cannot be less than cost price")
    return price
```

#### Putting It All Together
```python
from yaval import  validate, is_int,is_float

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
yaval comes with predefined validators that you can use right away. They are essentially factory functions that returns
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
              the standard python `re` package.  **Be careful when using this on untrusted input as you may expose
              yourself to regular expression DDos attacks**. 

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

   
### custom validators

#### A Note On Security 
_yaval is designed with adversarial users in mind and all built-in validators make no assumption about the input.
 When authoring custom validators, always make sure they're designed properly to handle malicious input_

In some situations where the built-in validators don't work for you, yaval allows you to define your own validator. 
Validators are essentially functions that take in a single input and return the newly validated input on success or 
raise a `yaval.ValidationException` for invalid input. A simple example maybe checking if a field is a valid
ip-address. 
```python
import re
from yaval import validate,is_str, ValidationException 

def is_ipv4_address(input):
    if not input:
        raise ValidationException("this field is required")
    input = str(input).strip()
    if not re.match(r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z", input):
        raise ValidationException("This field must be an ipv4 address")
    parts = input.split(".") 
    assert len(parts) == 4 # this should produce 4 parts else the regex test should have failed
    if any(int(part, base=10) > 255 for part in parts):
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
`yaval.validate` returns a tuple where the first element is an error and the second, the newly validated data. On successful 
validation, error is `None`. Errors are python dicts that follow exactly the structure of the schema so checking which field 
failed validation is trivial (as shown below). There's an extra field on the returned error  named `___hook` that holds 
errors raised by the optional hook function. 

**Example**
```python
from yaval import  validate, is_float, ValidationException

def hook(price):
    if price.get("selling_price") < price.get("cost_price"):
        raise ValidationException("selling_price cannot be less than cost_price")
    return price

price_schema = {
    "selling_price":is_float(required=True,round_to=2, min=0.01),
    "cost_price":is_float(required=True, round_to=2, min=0.01) 
}
# scenario 1
errors, _ = validate(schema=price_schema,data=dict(selling_price=0, cost_price=8), hook=hook)
print(errors) # {"selling_price":"'0' is less than minimum value required (0.1)"}

# scenario 2
errors, _ = validate(schema=price_schema,data=dict(selling_price=2, cost_price=8), hook=hook)
print(errors) # {"__hook":"selling_price cannot be less than cost_price"}

# scenario 3
_, validated_price = validate(schema=price_schema,data=dict(selling_price=12.159, cost_price=8.489), hook=hook)
print(validated_price) # {"selling_price":12.16, "cost_price":8.49}
```

### Testing 
```shell script
coverage run --source='.' -m pytest && coverage report 
```

### License
MIT

### contributing
Spot a bug? feature request? want to improve documentation? Kindly open an issue or make a pull request, your feedback 
is welcome.


