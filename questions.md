# Questions

#### Django questions
- Why serializers inherit form HyperlinkedModelSerializer ? Is it the best choice in this case?
- There is no caching for this app, when would you use it?



#### Python questions

- in `serializers.py` is it necessary to extract `StartDateEndDateOrderChecker` class? Does it promote readability? Will the code be better without it?


#### SQL questions

- Why are the tables normalized this way? Why is this approach good? What would be the different one?
- Intersection of intervals of dates is calculated on the python side, instead of database side. Why?
- When would you consider to calculate something on the side of database?
- Would the approach of pre-calculating dates be better (while storing results in separate table)?


#### Docker questions

- Explain the reason for usuing docker?
- Why docker-compose?
- What is docker swarm?


#### Tests questions

- Why there are no integration testing?
- Right now Model Mommy framework generates very limited set of data. What else would you test and how? i.e. names with apostrophee.


#### General code questions

- Current code allows for dates to be posted in the past. Why is this?


#### Cloud questions

- How would you design this app in the cloud? What will be different?
- What Redis is? When would you use it?