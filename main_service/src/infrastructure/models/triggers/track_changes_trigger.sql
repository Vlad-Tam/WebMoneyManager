CREATE OR REPLACE FUNCTION track_changes()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO change_tracker (changed_table, changed_id, changed_datetime, operation)
        VALUES (TG_TABLE_NAME, NEW.id, now(), TG_OP);
        RETURN null;
    END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER track_changes_transaction
    AFTER UPDATE OR INSERT OR DELETE
    ON transaction
    FOR EACH ROW
    EXECUTE FUNCTION track_changes();


CREATE TRIGGER track_changes_user
    AFTER UPDATE OR INSERT OR DELETE
    ON "user"
    FOR EACH ROW
    EXECUTE FUNCTION track_changes();


CREATE TRIGGER track_changes_category
    AFTER UPDATE OR INSERT OR DELETE
    ON category
    FOR EACH ROW
    EXECUTE FUNCTION track_changes();

