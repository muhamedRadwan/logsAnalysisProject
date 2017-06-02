# Logs Analysis Project

## Run IT !
### First install this modules
webapp2, paste, and webob
by **pip**:<br>
   1. `pip install webapp2`
   1. `pip install paste`
   1. `pip install webob`<br>
Add all files in the same dirctory in your vm then write in command line
`python main.py` <br>
Then enter to **127.0.0.1:8080** by your browser



## views that I created
    create view numOFaccessArticales as 
    select replace(path,'/article/','') as slug, count(path) as num from log  where path = path and 
    status = '200 OK'  and path like '/article%'
    group by path ;

    create view WriterOFArticle as 
    select t.slug,a.name from authors as a , articles as t
    where t.author = a.id ;

    create view AuthorsWithSlug as 
    select name,a.slug,num from WriterOFArticle as a
    join  numOFaccessArticales as n on a.slug =n.slug
    where a.slug = n.slug;


    create view BadRequests as
    select date(time) as day, count(*) as num 
    from log  where status != '200 OK'
    group by day;

    create view AllRequests as
    select date(time) as day, count(*) as num from log 
    group by day ;

    create view PrecentageOFRequests as 
    select a.day ,(b.num * 100 / a.num) as errors 
    from BadRequests as b , AllRequests as a
    where a.day=b.day;









