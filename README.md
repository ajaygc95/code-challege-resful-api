# Code-challege-resful-api
__Author__: gcajay95@gmail.com

I have used simple django rest framework to creat restful api for CRUD functionality of adding 
test cases to test suite by providing api link. 

**Three model/Database table used**
    
    1. TestCase
        To store test case info. We are going to use slug to fetch the data.
    
    2. TestSuiteItem
        Server purpose of middleware for final Test Suite list to store info of
        individual testcase

    3. TestSuites
        Final list of all added test cases list.

**Added basic authentication using drf TokenAuthentication. **



 ### Get Auth Token ###
    http://127.0.0.1:8000/auth/

 ### Create user or login ###
        GET --> http://127.0.0.1:8000/api/users/
        data :

        {   "username": "your user name",
            "password": "your password"
        },


 ### Post test cases ###
        POST --> http://127.0.0.1:8000/api/testcases/
        data :
`            {
            "title": "your title",
            "description": "your descriptions"
            }`

 ### Fetch test cases ###
        GET --> http://127.0.0.1:8000/api/testcases/

### Create a new test suite ###
    POST --> http://127.0.0.1:8000/api/test_suite_cases/

### Fetch a new test suite ###
    POST --> http://127.0.0.1:8000/api/test_suite_cases/
    
    Response --> Get list of all the test suite item inside test suite model

### Add test case item to Test suite given by pk"
    POST --> http://127.0.0.1:8000/api/test_suite_cases/7/
    
    provide tescast title or slug in the testcase field.
    data: {
            "testcase": "login" 
           }
    #slug: title or slug in the testcase detail.
    
    "message": "Test case has been appended to the Test Suite list"

    
### Get all testcase inside a Tes Suite ###

    GET --> http://127.0.0.1:8000/api/get_suite_items/1/ 
    provide pk of the testsuite 
    
    This is done by new View in Django make sure to check url that contains
    get_suite_items. 
    
    you should provide get_suite_items and PK of the test suite item. 
    
    This will give list of all the test case with detail
    
    {
        "pnp": {
            "id": 4,
            "title": "pnp",
            "slug": "pnp",
            "description": "prfile and preferences"
        },
        "homepage": {
            "id": 2,
            "title": "Homepage",
            "slug": "homepage",
            "description": "Page object model homepage"
        },
        "logout": {
            "id": 3,
            "title": "Logout",
            "slug": "logout",
            "description": "Logsout from the page"
        }
    }
    

### Delete test cases from suite ###
    DELETE --> http://127.0.0.1:8000/api/test_suite_cases/1/
    data: 
        { slug:"this is your title of test case name" }

### EDIT test cases from suite ###
    PUT --> http://127.0.0.1:8000/api/test_suite_cases/1/

    provide PK of test suite and add testcase item to testcase field

    data: {
        "testcase": "title"
    }

 ### Get Test Suite  Items  ###
    GET --> http://127.0.0.1:8000/api/get_suite_items/
    
    provide pk of the test sutie.
    
 ### Merge Two Test cases inside test suite  ###
    GET --> http://localhost:8000/api/merge_two_test/1/

    provide PK of the test suite and provide data as follows
    
    data : {
    "firstcase": "title",
    "secondcase": "title"
    }
-- 
    
    if you pass: sample test cases in the db . 

    {
    "firstcase": "pnp",
    "secondcase": "homepage"
    }
-- 

    Response: 
    {
        "pnpHomepage": {
            "pnp": {
                "id": 4,
                "title": "pnp",
                "slug": "pnp",
                "description": "prfile and preferences"
            },
            "homepage": {
                "id": 2,
                "title": "Homepage",
                "slug": "homepage",
                "description": "Page object model homepage"
            }
        }
    }
    

Tested with POSTMAN. 

Dockerfile and Docker compose are attached to this repo. might need to remove _0.0.0.0:8000_
from line #5
