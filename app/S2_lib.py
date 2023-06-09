# (A) LOAD SQLITE MODULE
import sqlite3, datetime
from calendar import monthrange
DBFILE = "SkateDB.db"

def checkConflicts(start,end):
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  confSQL = "SELECT * FROM BOOKING WHERE ((start >= ?) AND (end <= ?))"
  conflicts = cursor.execute(confSQL,(start,end)).fetchall()
  conn.close()
  if len(conflicts) == 0:
    return False
  else:
    return True

# (B) SAVE EVENT
def save (start, end, txt, color, bg, user_id, id=None):
  # (B1) CONNECT
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()

  # (B2) DATA & SQL
  data = (start, end, txt, color, bg, user_id)
  if id is None:
    sql = "INSERT INTO `Booking` (`start`, `end`, `text`, `color`, `bg`, `user_id`) VALUES (?,?,?,?,?,?)"
  else:
    sql = "UPDATE `Booking` SET `start`=?, `end`=?, `text`=?, `color`=?, `bg`=?, `user_id`=? WHERE `id`=?"
    data = data + (id,)

  # (B3) EXECUTE
  if checkConflicts(start, end):
    return False
  else:
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return True

# (C) DELETE EVENT
def delete(id):
  # (C1) CONNECT
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()

  # (C2) EXECUTE
  cursor.execute("DELETE FROM `Booking` WHERE `id`=?", (id,))
  conn.commit()
  conn.close()
  return True

# (D) GET EVENTS
def get(month, year, userID):
  # (D1) CONNECT
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()

  # (D2) DATE RANGE CALCULATIONS
  daysInMonth = str(monthrange(year, month)[1])
  month = month if month>10 else "0" + str(month)
  dateYM = str(year) + "-" + str(month) + "-"
  start = dateYM + "01 00:00:00"
  end = dateYM + daysInMonth + " 23:59:59"

  # (D3) GET EVENTS
  cursor.execute(
    "SELECT * FROM `Booking` WHERE ((`start` BETWEEN ? AND ?) OR (`end` BETWEEN ? AND ?) OR (`start` <= ? AND `end` >= ?)) AND user_id = ?",
    (start, end, start, end, start, end, userID)
  )
  rows = cursor.fetchall()
  if len(rows)==0:
    return None

  # s & e : start & end date
  # c & b : text & background color
  # t : event text
  data = {}
  for r in rows:
    data[r[0]] = {
      "s" : r[1], "e" : r[2],
      "c" : r[4], "b" : r[5],
      "t" : r[3], "uid" : r[6]
    }
  return data