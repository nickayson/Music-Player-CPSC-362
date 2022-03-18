CREATE TRIGGER SomeTriggerName ON table FOR INSERT AS
IF EXISTS (select * FROM inserted WHERE datefield='1/1/1900')
BEGIN
UPDATE T SET datefield=Null
FROM table T INNER JOIN inserted I ON T.idkey=I.idkey
WHERE I.datefield='1/1/1900'
END



