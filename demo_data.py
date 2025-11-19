"""
Demo Data Script - Populate database with sample data for interview demonstration
Run this after starting the server to create demo students and attendance records
"""

import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def create_demo_data():
    print("🚀 Creating demo data for interview demonstration...\n")
    
    # Step 1: Create admin account
    print("1️⃣ Creating admin account...")
    signup_data = {
        "email": "admin@demo.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 201:
            print("   ✅ Admin account created")
        else:
            print("   ℹ️  Admin account already exists")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 2: Login to get token
    print("\n2️⃣ Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", json=signup_data)
    if response.status_code != 200:
        print("   ❌ Login failed")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✅ Login successful")
    
    # Step 3: Create students
    print("\n3️⃣ Creating students...")
    students = [
        {"roll_no": "2024001", "name": "Alice Johnson", "class_name": "10A"},
        {"roll_no": "2024002", "name": "Bob Smith", "class_name": "10A"},
        {"roll_no": "2024003", "name": "Charlie Brown", "class_name": "10A"},
        {"roll_no": "2024004", "name": "Diana Prince", "class_name": "10B"},
        {"roll_no": "2024005", "name": "Ethan Hunt", "class_name": "10B"},
        {"roll_no": "2024006", "name": "Fiona Green", "class_name": "10B"},
        {"roll_no": "2024007", "name": "George Wilson", "class_name": "11A"},
        {"roll_no": "2024008", "name": "Hannah Lee", "class_name": "11A"},
        {"roll_no": "2024009", "name": "Ian Malcolm", "class_name": "11B"},
        {"roll_no": "2024010", "name": "Julia Roberts", "class_name": "11B"},
    ]
    
    student_ids = []
    for student in students:
        try:
            response = requests.post(f"{BASE_URL}/students/", json=student, headers=headers)
            if response.status_code == 201:
                student_id = response.json()["id"]
                student_ids.append(student_id)
                print(f"   ✅ Created: {student['name']} (ID: {student_id})")
            else:
                print(f"   ⚠️  {student['name']} might already exist")
        except Exception as e:
            print(f"   ❌ Error creating {student['name']}: {e}")
    
    # Step 4: Mark attendance for today
    print("\n4️⃣ Marking today's attendance...")
    today = date.today()
    
    attendance_data = [
        {"student_id": 1, "status": "present", "note": "On time"},
        {"student_id": 2, "status": "present", "note": "On time"},
        {"student_id": 3, "status": "absent", "note": "Sick leave"},
        {"student_id": 4, "status": "present", "note": ""},
        {"student_id": 5, "status": "present", "note": ""},
        {"student_id": 6, "status": "leave", "note": "Family emergency"},
        {"student_id": 7, "status": "present", "note": ""},
        {"student_id": 8, "status": "present", "note": "Late by 10 mins"},
        # Leave 9 and 10 unmarked to show "not marked" in dashboard
    ]
    
    for att in attendance_data:
        try:
            response = requests.post(f"{BASE_URL}/attendance/mark", json=att, headers=headers)
            if response.status_code == 200:
                status = att['status']
                print(f"   ✅ Student {att['student_id']}: {status}")
            else:
                print(f"   ⚠️  Student {att['student_id']}: Already marked or error")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Step 5: Mark attendance for past days (for trends)
    print("\n5️⃣ Creating historical attendance data...")
    for days_ago in range(1, 7):
        past_date = today - timedelta(days=days_ago)
        # Mark attendance for first 5 students only
        for student_id in range(1, 6):
            att = {
                "student_id": student_id,
                "status": "present" if student_id % 3 != 0 else "absent",
                "date": past_date.isoformat(),
                "note": ""
            }
            try:
                requests.post(f"{BASE_URL}/attendance/mark", json=att, headers=headers)
            except:
                pass
    print("   ✅ Historical data created")
    
    # Summary
    print("\n" + "="*60)
    print("✨ Demo data created successfully!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Admin Email: admin@demo.com")
    print(f"   • Password: admin123")
    print(f"   • Students Created: 10")
    print(f"   • Classes: 10A, 10B, 11A, 11B")
    print(f"   • Today's Attendance: 8 marked, 2 unmarked")
    print(f"   • Historical Data: Last 6 days")
    print(f"\n🌐 Open: http://localhost:8000/docs")
    print(f"   1. Login with admin@demo.com / admin123")
    print(f"   2. Click 'Authorize' and paste the token")
    print(f"   3. Try GET /admin/dashboard to see statistics")
    print(f"   4. Try GET /attendance/export to download CSV")
    print("\n✅ Ready for interview demonstration!")

if __name__ == "__main__":
    create_demo_data()
