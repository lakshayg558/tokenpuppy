select tc.column_name from information_schema.table_constraints tk,information_schema.key_column_usage tc
where tk.constraint_type = 'PRIMARY KEY'
and tk.table_name = ANY(%s) and tk.table_name = tc.table_name