import bcrypt
from app.db_utils import SqlEngine


class PasswordSecurity():
  def __init__(self,user_id,input_pass):
      self.user_id = user_id
      self.input_pass= input_pass

  def pass_hashing(self):
      hashed_pass = bcrypt.hashpw(self.input_pass.encode(), bcrypt.gensalt(rounds=12))
      return hashed_pass.decode()

  def pass_verify(self):
      hashed_pass = SqlEngine().sql_engine("sql/custom_queries/hashed_pass.sql", ([self.user_id.upper()],))
      verification_result = bcrypt.checkpw(self.input_pass.encode(), hashed_pass[0][0].encode("utf-8"))
      return verification_result




