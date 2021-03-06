# MIZRAPP

```
A repository for the hackathon project

https://mizrapp.herokuapp.com/
```

## Setup Restfull service

```
Run this command inside api folder 

Create virtual env

	virtualenv venv

Actviate virtual env

	source venv/bin/activate

Install requirements

	pip3 install -r requirements.txt


```

## Documentation of our restfull API

### #Login
```
[POST] /login

Request

{
    email : String,
    password : String
}

Response

{
    _id : ObjectID,
    email : String,
    name : String,
    token : String
}

Errors

{
	message : 'User not found'
}

{
	message : 'Wrong password'
}

```

### #Registeration
```
[POST] /register

Request

{
    email : String,
    password : String,
    name : String
}

Response

{
    _id : ObjectID,
    email : String,
    name : String,
    token : String
}

Errors

{
	message : 'Email exists'
}

```

```
This token will be used on authorizon field of each request header

Error

{
	message : 'Invalid Token'
}
```

### #User Information
```
This request will be sent after first login.

[POST] /api/user/info

Request

{   
    user : String | {userId}
    age : integer,
    profession : String,
    gender : String | {Male or Female},
    city : String
}

Reponse status code 200
```

### #Initial App Data
```
[GET] /api/users/{userId}

Response

{
    categories : {
        {
            _id : ObjectID,
            name : String,
            subCategories : [
                {
                    _id : ObjectID,
                    name : String,
                }
            ]
        }
    },
    reviews : [
			{
				_id : ObjectID,
				product : ObjectID,
				isUsed : boolean,
				rank : integer | 1 to 5,
				minPrice : integer | lira,
				maxPrice : integer | lira,
				user : ObjectID
			}
		]
}
```

### #Get products list with sub category

```
[GET] /api/products/{subCategoryID}

Response

{
    products : [
        {
            _id : ObjectID,
            name : String,
            desc : String,
            price : integer | lira,
						discount : integer | lira,
            photo : String,
            company : ObjectID,
            subCategory : ObjectID
            ...
        }
    ]
}
```


### #Post product review

```

[POST] /api/products/review

Request

{
    product : String | {productID},
    isUsed : boolean,
    rank : integer | {1 to 5},
    offer : integer | {lira},
    user : String | {userID}
}

response status code 200
```


### #Get Images

```

[GET] /api/images/{productId}{type}

```


## Datebase Migrations

### User - users

```
{
    _id : ObjectID,
    name : String,
    email : String,
    password : String
}
```

### User Info - user_info

```
{
    _id : ObjectID,
    user : ObjectID,
    age : Integer,
    profession : String,
    gender : String | Male or Female,
    city : String
}
```

### Category - categories

```
{
    _id : ObjectID,
    name : String,
    subCategories : Array | ObjectID
}
```

### Company - companies

```
{
    _id : ObjectID,
    name : String,
    type : String | jpg or png
}
```

### SubCategory - subcategories

```
{
    _id : ObjectID,
    name : String,
}
```

### Product - products

```
{
    _id : ObjectID,
    name : String,
    desc : String,
    price : integer | lira,
		discount : integer | lira,
    photo : String,
    company : ObjectID,
    subCategory : ObjectID
		type : String | jpg or png
}
```

### Review - reviews

```
{
    _id : ObjectID,
    product : ObjectID,
    isUsed : boolean,
    rank : integer | 1 to 5,
    offer : integer | lira,
    user : ObjectID
}
```
