Pyval - Easy data validation 

#Motivation 
There are many libraries available for validating data in python such as pydantic, volouptous, validino, jsonvalidator,
but they all surprisingly require too much boilerplate and code ceremony. The goal of this library is provide a much easy 
and simple to use alternative for data validation. 


## Getting Started

```python
    from datetime import datetime
    from pyval import Schema, validators

    repo = {"name":"Pyval", "version":"0.0.1", "stars":"2000", "last_published":"2021-02-02", "languages":["python","c++"]} 
    repo_schema = Schema({
        "name":validators.is_str(min_length=3, max_length=8, trim=True, required=True),
        "version":validators.is_str(required=True, pattern=r"\d+\\.\d+\\.\d+"),
        "stars":validators.is_int(required=False, min=0, default=0),
        "last_published":validators.is_date(required=False, max=datetime.today(), format="%Y-%m-%d"),
        "languages": validators.is_list(required=False, min_length=1, validator=validators.is_str(trim=True,min_len=1))
    })
    
    errors, validated_repo = repo_schema.validate(data=repo)
    if errors: #validation failed
        for field, msg in errors:
            print(field, msg)
    else:
        use_validated_data_somehow(validated_repo)
```

### Schemas

#### Defining Schemas

#### Hooks


### Validators

#### is_str 

#### is_int

#### is_float

#### is_date

#### is_list

#### is_dict

#### custom validators

### Handling Errors 


#### contribution

