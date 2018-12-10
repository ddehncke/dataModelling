/* RESTAURANTS WITH HIGHEST RATING. DISPLAYING ALSO THE CATEGORIES LINKED TO CATEGORIES */

 WITH table_ as (
	SELECT rest.name as restaurant, ROUND(AVG(re.evaluation),2) as average_stars, COUNT(re.id_review) as reviews, rest.cusine as cusine
	FROM restaurant rest, review re
	WHERE rest.id_business = re.business
	GROUP BY rest.name, rest.cusine
	ORDER BY average_stars DESC
)
	SELECT *
	FROM table_
	WHERE reviews > 3000;

/* RESTAURANTS WITH HIGHEST RATING. DISPLAYING ALSO THE CATEGORIES LINKED TO CATEGORIES */

WITH table_ as (
	SELECT rest.name as restaurant, ROUND(AVG(re.evaluation),2) as average_stars, COUNT(re.id_review) as reviews, rest.attribute as attribute
	FROM restaurant rest, review re
	WHERE rest.id_business = re.business
	GROUP BY rest.name, rest.attribute
	ORDER BY average_stars DESC
)
	SELECT *
	FROM table_
	WHERE reviews > 500;

/* BEST RESTAURANTS DIVIDED FROM POSTAL_CODE */
WITH table_ as (
	SELECT rest.postal_code, rest.name, COUNT(re.id_review) as reviews
	FROM restaurant rest, review re
	WHERE rest.id_business = re.business
	GROUP BY rest.postal_code, rest.name
	ORDER BY reviews DESC
)
	SELECT *
	FROM table_
	WHERE reviews > 500;

/* GET AVERAGE EVALUATION FOR CATEGORY African */

SELECT COUNT(re.id_review) as N°reviews, ROUND(AVG(re.evaluation), 2) as average_stars
FROM restaurant rest, review re
WHERE rest.id_business = re.business
AND rest.cusine @> ARRAY['Chinese']
ORDER BY N°reviews, average_stars DESC

/* LATITUDE AND LONGITUDE FROM GEOGRAPHY */

SELECT rest.name, rest.geog, ST_X(rest.geog::geometry) as latitude, ST_Y(rest.geog::geometry) as longitude FROM restaurant rest;

/* STRUCTURE OF THE ANALYSIS */

/*

PRE PROCESSING
1_ Talk about the dataset (yelp)
2_ How we structured our database (talk about sql schema and POSTGIS and see our tables)
3_ Define our main scope (We would like to open a new restaurant (in a randomly area))
4_ Define what s important to reach the scope
5_ Describing the queries than we used
6_ Discuss about tableau
7_ Present results
8_ Compare tableau and POSTGRES (?)
9_ Conclusions


7_ Present results
  A_
    1_ Present the spatial informations about the entire dataset (display in a map the restaurants)
    2_ Divide the spatial informations in regions (USA and EU)
    3_ Show the main results grouped by area (5 most common cusine, 5 highest reated cusine, 5 most famous restaurants, 5 highest cusine)
  B_
    1_ Present the results analyzing over the time
    2_ Changing of common cusines over time
    3_ Changing of highest rated cusine over time
    4_ The same for the restaurants

EXAMPLE
1_ Open a restaurant in a specific city
2_ Looking for all the needed information about that city (like: Opened restaurants, cusines, attributes...)
3_ Compare the city with 5 other cities with the same informations
4_FINAL_ Talk about results and make some suggests

*/