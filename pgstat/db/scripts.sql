-- PROCEDURE: public.save_stats()
-- DROP PROCEDURE IF EXISTS public.save_stats();

CREATE OR REPLACE PROCEDURE public.save_stats()
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
	WITH statements AS (
		SELECT
			*
		FROM
			pg_stat_statements
		INNER JOIN
			pg_roles on (userid=pg_roles.oid)
		INNER JOIN
			pg_database on (dbid=pg_database.oid)
	),
	queries AS (
		INSERT INTO
			statcollector_queries (queryid, userid, dbid, query)
		SELECT
			queryid, userid, dbid, query
		FROM
			statements
		ON CONFLICT DO NOTHING
	)
	INSERT INTO statcollector_last_statement
		(dbid,userid,queryid, toplevel, plans, calls,
		 total_plan_time, total_exec_time,
		 rows,shared_blks_hit,shared_blks_read,shared_blks_dirtied,shared_blks_written,local_blks_hit,
		 local_blks_read,local_blks_dirtied,local_blks_written,temp_blks_read,temp_blks_written,reset_time)
	 SELECT
	 	 dbid, userid, queryid, toplevel, plans,  calls,
		 total_plan_time,total_exec_time,
		 rows, shared_blks_hit, shared_blks_read,
		 shared_blks_dirtied, shared_blks_written, local_blks_hit,
		 local_blks_read, local_blks_dirtied, local_blks_written, temp_blks_read, temp_blks_written,
		 (pg_stat_statements_info()).stats_reset
	 FROM statements
	 ON CONFLICT ON CONSTRAINT dbid_userid_queryid_toplevel_unique_reset_time_unq
	 DO UPDATE
	 SET datecr = EXCLUDED.datecr,
	 	plans = EXCLUDED.plans,
		calls = EXCLUDED.calls,
		total_plan_time = EXCLUDED.total_plan_time,
		total_exec_time = EXCLUDED.total_exec_time,
		rows = EXCLUDED.rows,
		shared_blks_hit = EXCLUDED.shared_blks_hit,
		shared_blks_read = EXCLUDED.shared_blks_read,
		shared_blks_dirtied = EXCLUDED.shared_blks_dirtied,
		shared_blks_written = EXCLUDED.shared_blks_written,
		local_blks_hit = EXCLUDED.local_blks_hit,
		local_blks_read = EXCLUDED.local_blks_read,
		local_blks_dirtied = EXCLUDED.local_blks_dirtied,
		local_blks_written = EXCLUDED.local_blks_written,
		temp_blks_read = EXCLUDED.temp_blks_read,
		temp_blks_written = EXCLUDED.temp_blks_written
    WHERE calls < EXCLUDED.calls;
END;
$BODY$;

-- FUNCTION: public.statements_after_iud()
-- DROP FUNCTION IF EXISTS public.statements_after_iud();
CREATE OR REPLACE FUNCTION public.statements_after_iud()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
begin
	if TG_OP = 'INSERT' then

		insert into statcollector_statement_details
			(datecr, dbid,userid,queryid, toplevel, plans, calls,
			 total_plan_time,total_exec_time,
			 rows,shared_blks_hit,shared_blks_read,
			 shared_blks_dirtied,shared_blks_written,local_blks_hit,local_blks_read,
			 local_blks_dirtied,local_blks_written,temp_blks_read,temp_blks_written)
		values
			(NEW.datecr, NEW.dbid,
			NEW.userid, NEW.queryid, NEW.toplevel,
			NEW.plans,  NEW.calls,
			NEW.total_plan_time,
			NEW.total_exec_time,
			NEW.rows, NEW.shared_blks_hit,
			NEW.shared_blks_read, NEW.shared_blks_dirtied,
			NEW.shared_blks_written, NEW.local_blks_hit,
			NEW.local_blks_read, NEW.local_blks_dirtied,
			NEW.local_blks_written, NEW.temp_blks_read,
			NEW.temp_blks_written);
		return NEW;
	elseif TG_OP = 'UPDATE' then

		insert into statcollector_statement_details
			(datecr, dbid,userid,queryid, toplevel, plans, calls,
			 total_plan_time,total_exec_time,
			 rows,shared_blks_hit,shared_blks_read,
			 shared_blks_dirtied,shared_blks_written,local_blks_hit,local_blks_read,
			 local_blks_dirtied,local_blks_written,temp_blks_read,temp_blks_written)
		values
			(NEW.datecr,
			 NEW.dbid,
			 NEW.userid,
			 NEW.queryid,
			 NEW.toplevel,
			 NEW.plans - OLD.plans,
			 NEW.calls - OLD.calls,
			 NEW.total_plan_time - OLD.total_plan_time,
			 NEW.total_exec_time - OLD.total_exec_time,
			 NEW.rows - OLD.rows,
			 NEW.shared_blks_hit - OLD.shared_blks_hit,
			 NEW.shared_blks_read - OLD.shared_blks_read,
			 NEW.shared_blks_dirtied - OLD.shared_blks_dirtied,
			 NEW.shared_blks_written - OLD.shared_blks_written,
			 NEW.local_blks_hit - OLD.local_blks_hit,
			 NEW.local_blks_read - OLD.local_blks_read,
			 NEW.local_blks_dirtied - OLD.local_blks_dirtied,
			 NEW.local_blks_written - OLD.local_blks_written,
			 NEW.temp_blks_read - OLD.temp_blks_read,
			 NEW.temp_blks_written - OLD.temp_blks_written);
		return NEW;
	end if;
	return OLD;
end;
$BODY$;