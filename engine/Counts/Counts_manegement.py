from sqlalchemy.orm import sessionmaker
from database.database import Users,Counts,Counts_registration,engine

Session = sessionmaker(bind=engine)

session = Session()

def create_count(user:int,value:float,divisions:float,payment_day:str,description:str,active=True):
  new_count = Counts(owner=user,value=value,divisions=divisions,payment_day=payment_day,description=description,active=active)
  session.add(new_count)
  session.commit()

  return True

def load_count(user:int):
  active_count = session.query(Counts).filter(Counts.owner==user,Counts.active==True).all()

  if active_count:
    return active_count
  else:
    return False
  
def query_user_by_count_owner_id(user_id:int):
  existing_user = session.query(Users).filter(Users.id == user_id).first()


  if existing_user:
    return existing_user
  else:
    return False
  
def counts_modification(count_id:int,user_id:int,payment_date:str=None,description:str=None,value:float=None,divisions:float=None):
  existing_count = session.query(Counts).filter(Counts.id==count_id,Counts.owner==user_id).first()
  if existing_count:
    if payment_date != None:
      existing_count.payment_day = payment_date
    if description != None:
      existing_count.description = description
    if value != None:
      existing_count.value = value
    if divisions != None :
      existing_count.divisions = divisions
    session.commit()
    return True

def delete_count(count_id:int,user_id:int):
  existing_count = session.query(Counts).filter(Counts.id==count_id,Counts.owner==user_id).first()
  if existing_count:
    session.delete(existing_count)
    session.commit()
    return True
  else:
    return False
  
def pay_count(count_id:int,user_id:int,payment=True,date:str=None):
  existing_payment = session.query(Counts_registration).filter(Counts_registration.owner==user_id,Counts_registration.count_id==count_id,Counts_registration.payment_confirmed_date == date).first()
  if existing_payment:
    return False
  else:
    new_payment = Counts_registration(owner=user_id,count_id=count_id,payment=payment,payment_confirmed_date=date)
    session.add(new_payment)
    session.commit()
    unactivate_count(count_id,user_id)
    return True
  
def load_divisions_payed(user:int):
  active_counts = session.query(Counts_registration).filter(Counts_registration.owner==user,Counts_registration.payment==True).all()
  if active_counts:
    return active_counts
  else:
    return False
  
def load_count_infos(count_id:int,user_id:int):
  count = session.query(Counts).filter(Counts.owner==user_id,Counts.id == count_id).first()
  if count:
    return count
  else:
    return False
  
def load_payed_count_infos(count_id:int,user_id:int):
  try:
    count = session.query(Counts_registration).filter(Counts_registration.owner==user_id,Counts_registration.count_id == count_id).all()
    if count:
      return count
    else:
      return False
  except:
    return []
  
def delete_confirmed_payment(count_id:int,user_id:int,date:str):
  count = session.query(Counts_registration).filter(Counts_registration.owner==user_id,Counts_registration.count_id==count_id,Counts_registration.payment_confirmed_date==date).first()
  if count:
    session.delete(count)
    session.commit()
    return True
  else:
    return False
  
def unactivate_count(count_id:int,user_id:int):
  contas_pagas = load_payed_count_infos(count_id,user_id)
  Total_a_ser_pago = load_count_infos(count_id,user_id)
  if len(contas_pagas) == Total_a_ser_pago.divisions:
    Total_a_ser_pago.active = False
    session.commit()
    return True
