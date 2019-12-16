-----------------------------

DROP FUNCTION IF EXISTS entity_save CASCADE;

CREATE FUNCTION entity_save() RETURNS trigger AS $entity_save$
    DECLARE
    	title_full VARCHAR(2000);
		title_short VARCHAR(2000);
		title_search VARCHAR(4001);

    BEGIN
        title_full := REGEXP_REPLACE(NEW.title_full, '[^\w\d\s]+', ' ', 'g');
        title_short := REGEXP_REPLACE(NEW.title_short, '[^\w\d\s]+', ' ', 'g');
        title_search := UPPER(CONCAT(title_full, ' ', title_short));
        title_search := REGEXP_REPLACE(title_search, '\s+', ' ', 'g');
        NEW.title_short := REGEXP_REPLACE(NEW.title_short, '\s+', ' ', 'g');
        NEW.title_full := REGEXP_REPLACE(NEW.title_full, '\s+', ' ', 'g');
        NEW.title_search := title_search;
        RETURN NEW;
    END;
$entity_save$ LANGUAGE plpgsql;

CREATE TRIGGER entity_save BEFORE INSERT OR UPDATE ON directory_entity
    FOR EACH ROW EXECUTE PROCEDURE entity_save();

----------------------------

DROP FUNCTION IF EXISTS kso_save CASCADE;

CREATE FUNCTION kso_save() RETURNS trigger AS $kso_save$

	DECLARE
    	title_full VARCHAR(1000);

    BEGIN
    	IF NEW.entity_id IS NOT NULL THEN
    		SELECT directory_entity.title_full INTO title_full
    		    FROM directory_entity WHERE id = NEW.entity_id;
    		NEW.title_full := title_full;
	    END IF;
		NEW.title_search := UPPER(CONCAT(NEW.title_full, ' ', NEW.title_short));
        RETURN NEW;
    END;
$kso_save$ LANGUAGE plpgsql;

CREATE TRIGGER kso_save BEFORE INSERT OR UPDATE ON directory_kso
    FOR EACH ROW EXECUTE PROCEDURE kso_save();
