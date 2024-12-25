from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Device(BaseModel):
  id: int
  barcod: str
  item: str
  item_description:str
  category: str
  manufacturer:str
  model_No: str
  serial_No: int
  department: str
  calib_status: str
  calib_cert_No: int
  calib_Exp_Date: str
  
def setup_database():
  try:
    conn = sqlite3.connect('devices.db') # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor() # إنشاء مؤشر
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcod TEXT NOT NULL,
            item TEXT NOT NULL,
            item_description TEXT,
            category TEXT Null,
            manufacturer TEXT Null,
            model_No TEXT,
            serial_No INTEGER,
            department TEXT Null,
            calib_status TEXT Null,
            calib_cert_No INTEGER Null,
            calib_Exp_Date TEXT Null
        )
    ''')
    conn.commit() # حفظ التغييرات
  except sqlite3.Error as e:  # التعامل مع الأخطاء المحتملة
    print(e)  # طباعة الخطأ
    return {"error": "Failed to fetch device"}  # إرجاع رسالة خطأ في حالة فشل جلب البيانات

setup_database()

@app.get("/device/")
async def read_device():
  try:
    conn = sqlite3.connect('devices.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر (cursor) للتفاعل مع قاعدة البيانات
    cursor.execute("SELECT * FROM devices")  # تنفيذ استعلام SQL لجلب جميع الصفوف من جدول devices
    rows = cursor.fetchall()  # جلب جميع النتائج من قاعدة البيانات
    conn.close()  # إغلاق الاتصال بقاعدة البيانات
    return rows  # إرجاع البيانات التي تم جلبها من قاعدة البيانات
  except sqlite3.Error as e:  # التعامل مع الأخطاء المحتملة
    print(e)  # طباعة الخطأ
    return {"error": "Failed to fetch devices"}  # إرجاع رسالة خطأ في حالة فشل جلب البيانات
 

@app.post("/device/")
async def create_device(device: Device):
  try:
      conn = sqlite3.connect('devices.db')
      cursor = conn.cursor()
      cursor.execute("INSERT INTO devices (barcod,item,item_description,category,manufacturer,model_No,serial_No,department,calib_status,calib_cert_No,calib_Exp_Date) VALUES (?,?,?, ?,?,?, ?,?, ?,?,?)", (device.barcod,device.item,device.item_description,device.category,device.manufacturer,device.model_No,device.serial_No,device.department,device.calib_status,device.calib_cert_No,device.calib_Exp_Date))
      conn.commit()
      conn.close()
      return {"message": "Device added successfully"}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to create device"}


@app.put("/devices/{device_id}")
async def update_device(device_id: int, device: Device):
  try:
    conn = sqlite3.connect('devices.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر
    cursor.execute("UPDATE devices SET barcod = ?, item = ?,item_description = ?,category =?,manufacturer = ?,model_No = ?,serial_No = ?,department = ?,calib_status = ?,calib_cert_No = ?,calib_Exp_Date = ? WHERE id = ?",(device.barcod,device.item, device.item_description,device.category,device.manufacturer,device.model_No,device.serial_No,device.calib_status,device.calib_cert_No,device.calib_Exp_Date, device_id))  #SQL لتحديث بيانات جهاز]
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    conn.close()  # إغلاق الاتصال
    return {"id": device_id, **device.dict()}  # إرجاع بيانات الطالب المحدثة
  except sqlite3.Error as e:  # في حالة حدوث خطأ
    print(e)  # طباعة الخطأ
    return {"error": "Failed to update device"}  # إرجاع رسالة خطأ

@app.delete("/devices/{device_id}")
async def delete_devices(device_id: int):
  try:
    conn = sqlite3.connect('devices.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر
    cursor.execute("DELETE FROM devices WHERE id = ?", (device_id,))  # تنفيذ استعلام SQL لحذف طالب
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    conn.close()  # إغلاق الاتصال
    return {"message": "Device deleted"}  # إرجاع رسالة تأكيد الحذف
  except sqlite3.Error as e:  # في حالة حدوث خطأ
    print(e)  # طباعة الخطأ
    return {"error": "Failed to delete device"}  # إرجاع رسالة خطأ
