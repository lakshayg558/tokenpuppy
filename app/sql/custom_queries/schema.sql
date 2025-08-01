SELECT column_name
FROM information_schema.columns
WHERE table_name = ANY(%s)
Order by ordinal_position