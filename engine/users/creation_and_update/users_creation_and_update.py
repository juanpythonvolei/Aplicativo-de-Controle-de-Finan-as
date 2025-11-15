from sqlalchemy.orm import sessionmaker
from database.database import Users,engine

Session = sessionmaker(bind=engine)

session = Session()


def create_user(user:str,password:str):
  if session.query(Users).filter(Users.username==user).first():
    return False
  else:
    new_user = Users(username=user,password=password)
    session.add(new_user)
    session.commit()
    return True
  

def update_user_password_username(user:int,new_password:str=None,new_username:str=None):
  existing_user = session.query(Users).filter(Users.id == user).first()
  if existing_user:
    if new_password != None and new_username != None:
      existing_user.username = new_username
      existing_user.password = new_password
      session.commit()
      session.close()
      return True
    elif new_password and new_username == None:
      existing_user.password = new_password
      session.commit()
      session.close()
      return True
    elif new_username and new_password == None:
      existing_user.username = new_username
      session.commit()
      session.close()
      return True
  return False

def search_user(username:str):
  existing_user = session.query(Users).filter(Users.username == username).first()
  if existing_user:
    return existing_user
  else:
    return False
  
def delete_user(user_id = int):
  user = session.query(Users).filter(Users.id ==user_id).first()
  if user:
    session.delete(user)
    session.commit()
    session.close()
    return True
  else:
    return False