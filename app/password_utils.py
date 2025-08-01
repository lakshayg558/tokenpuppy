import bcrypt
from app.db_utils import SqlEngine, CrudOperations
from config import user_threshold

class PasswordSecurity():
  def __init__(self,user_id,input_pass):
      self.user_id = user_id
      self.input_pass= input_pass
      self.count = int(SqlEngine().sql_engine("sql/custom_queries/lock_count.sql", ([self.user_id.upper()],))[0][0])


  def pass_hashing(self):
      hashed_pass = bcrypt.hashpw(self.input_pass.encode(), bcrypt.gensalt(rounds=12))
      return hashed_pass.decode()

  def pass_verify(self):
      hashed_pass = SqlEngine().sql_engine("sql/custom_queries/hashed_pass.sql", ([self.user_id.upper()],))
      if hashed_pass == []:
        return "User name doesn't Exist.Please Sign up or Contact Admin"
      else:
        verification_result = bcrypt.checkpw(self.input_pass.encode(), hashed_pass[0][0].encode("utf-8"))
        return verification_result

class PassTracking(PasswordSecurity):
    def lock_account(self):
        if ((self.count <= (user_threshold-2)) or (self.count == None)) and (self.pass_verify() == False):
            CrudOperations("sysuser", {"Unsuccess_count": self.count+1}).update(self.user_id)
            return f"Wrong Password.You have {user_threshold- (self.count+1)} attempts left"
        elif ((self.count >= user_threshold -1 ) and (self.pass_verify() == False)):
            CrudOperations("sysuser", {"Unsuccess_count": self.count + 1, "disable": "Y"}).update(self.user_id)
            return f"Wrong Password.You are locked because of Wrong password is entered multiple times.Please contact Admin"


