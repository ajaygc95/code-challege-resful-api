# Code-challege-resful-api

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

 ### Post test cases ###
        POST --> http://127.0.0.1:8000/api/testcases/
        data :
`            {
            "title": "your title",
            "description": "your descriptions"
            }`

 ### Fetch test cases ###
        GET --> http://127.0.0.1:8000/api/testcases/

 ### Create user or login ###
        GET --> http://127.0.0.1:8000/api/users/
        data :

        {   "username": "your user name",
            "password": "your password"
        },

 ### Add test cases ###
    POST --> http://127.0.0.1:8000/api/test_suite_cases/{pass your slug here itself}/
    data: 
        { slug:"this is your title of test case name" }

### Delete test cases from suite ###
    DELETE --> http://127.0.0.1:8000/api/test_suite_cases/{pass your slug here itself}/
    data: 
        { slug:"this is your title of test case name" }

### EDIT test cases from suite ###
    PUT --> http://127.0.0.1:8000/api/test_suite_cases/{pass your slug here itself}/
    data: 
        { slug:"this is your title of test case name" }

 ### Get Test Suite  Items  ###
          GET --> http://127.0.0.1:8000/api/get_suite_items/  


Tested with POSTMAN. 
