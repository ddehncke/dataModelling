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