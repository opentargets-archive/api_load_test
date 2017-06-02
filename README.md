TEST URLS
---------
mixed url set composition: test_urls.txt

1000 search for gene symbol or name
100 best hit search with multiple gene symbols or name | hard for es, but should work with no issues
1000 association filter queries with pagination up to 10000
1000 evidence filter queries with pagination up to 10000
50 evidence filter queries with pagination up to 5M | very hard for elasticsearch it can crush the cluster
250 enrichment calls with a set of random genes | cache is active and it tests having enough memory in redis to store the cache

HOW TO RUN
----------

GET your JWT Auth Token with a massive allowance

`http http://api-us-east.opentargets.io/api/latest/public/auth/request_token?app_name=load-test&secret=yoursecrethere`

Launch with Siege like this:

`siege -f test_urls.txt -c 32 -d 3 -i -v -H "Auth-Token: my.supersecret.jwt"`

it will open 32 connections, and each one will call a random line from the file with a random delay of up to 3 seconds.
