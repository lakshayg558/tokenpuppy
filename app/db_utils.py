import logging
from app.db_connection import DBConnection

class SqlEngine(DBConnection):
    def __init__(self):
        super().__init__()
    def sql_engine(self, filepath, parameter):
        try:
            with open (filepath,'r') as file:
                sql_file = file.read()
                self.cursor.execute(sql_file, parameter)
                sql_result = self.cursor.fetchall()
            return sql_result
        except Exception as e:
            logging.error(f"I am having Issues executing the SQL Query {filepath} and <{sql_file}> parameter {parameter} because of {e}")
        finally:
            DBConnection.close(self)

    def sql_engine_string(self, statement_string, parameter):
        try:
            self.cursor.execute(statement_string, parameter)
            self.conn.commit()
        except Exception as e:
            logging.error(f"I am having Issues executing the SQL Query {statement_string} for  parameter {parameter} because of {e}")
        finally:
            DBConnection.close(self)

class PrimaryKeyGenerator():
    def __init__(self,tablename):
        self.tablename = tablename

    @staticmethod
    def tuple_list_convert(input_tuple_list):
        output_list = []
        for tuple in input_tuple_list:
            output_list.append(tuple[0])
        return output_list

    @staticmethod
    def tuple_list_convert_M2(input_tuple_list):
        output_list = []
        for tuple in input_tuple_list[0]:
            output_list.append(tuple)
        return output_list

    def primary_key_gen(self):
        column_name = SqlEngine().sql_engine("sql/custom_queries/schema.sql",(['metadata'],))
        column_name_list = PrimaryKeyGenerator('sysuser').tuple_list_convert(column_name)
        primary_key_data_Set = SqlEngine().sql_engine("sql/custom_queries/metadata_tablename.sql", ([self.tablename],))
        primary_key_data_Set_list = PrimaryKeyGenerator('sysuser').tuple_list_convert_M2(primary_key_data_Set)
        #last_record = self.cursor.execute(f"Select * from {tablename} ORDER BY createdt limit 1").fetchone()
        pk_dict_meta = dict(zip(column_name_list, primary_key_data_Set_list))
        if pk_dict_meta.get('incremental_flag') != 'N':
            return pk_dict_meta

class CrudOperations():
    def __init__(self, tablename, input_dict ):
        self.tablename = tablename
        self.input_dict = input_dict

    @staticmethod
    def dict_statement_update_body(input_dict):
        column_value = ""
        for key in input_dict.keys():
            column_value += f" {key} = %s ,"
        return(column_value[:-1])

    @staticmethod
    def dict_statement_insert_body(input_dict):
        column_value = ""
        for key in input_dict.keys():
            column_value += f" {key} ,"
        return (column_value[:-1])

    @staticmethod
    def dict_statement_insert_value(input_dict):
        placeholder = ""
        for num in range(0,len(input_dict)):
            placeholder += "%s ,"
        return placeholder[:-1]

    @staticmethod
    def dict_statement_value(input_dict,primary_key_value = None):
        column_value = ""
        for key in input_dict.keys():
            column_value += f"{input_dict[key]},"
        if primary_key_value != None:
            column_value += primary_key_value
        else:
            column_value
        return column_value.split(",")

    def update(self,primary_key_value):
        primary_key_column = SqlEngine().sql_engine("sql/custom_queries/primary_key.sql",([self.tablename],))
        updating_parm = self.dict_statement_update_body(self.input_dict)
        update_value = self.dict_statement_value(self.input_dict,primary_key_value)
        print(update_value)
        update_statement = f"update {self.tablename} set {updating_parm} where {primary_key_column[0][0]} = %s"
        SqlEngine().sql_engine_string(update_statement, update_value)

    def insert(self):
        insert_statement_body = f"INSERT INTO {self.tablename} ({self.dict_statement_insert_body(self.input_dict)}) VALUES ({self.dict_statement_insert_value(self.input_dict)})"
        SqlEngine().sql_engine_string(insert_statement_body, self.dict_statement_value(self.input_dict))

    def insert_custom_pk(self):
        pass


