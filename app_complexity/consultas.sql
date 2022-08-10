#### 1 nível ####
SELECT
	relative_path,
	(
	SELECT
		count(id)
	from
		app_metrics_filedependsonfile amf2
	where
		destination_id = amf.id) AS nr_dependencies
from
	app_metrics_file amf
order by
	nr_dependencies DESC
limit 7

#### 2 niveis ###
