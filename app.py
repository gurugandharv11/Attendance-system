from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/attendance_db'
db = SQLAlchemy(app)

# Student Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)

# Attendance Table
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))

# API: Mark Attendance
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student = Student.query.filter_by(roll_no=data['roll_no']).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    attendance = Attendance(student_id=student.id, status='Present')
    db.session.add(attendance)
    db.session.commit()

    return jsonify({'message': f'Attendance marked for {student.name}'})

# API: Analytics
@app.route('/analytics/<roll_no>', methods=['GET'])
def analytics(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    total = Attendance.query.filter_by(student_id=student.id).count()
    present = Attendance.query.filter_by(student_id=student.id, status="Present").count()
    percentage = (present / total * 100) if total > 0 else 0

    return jsonify({
        'student': student.name,
        'total_classes': total,
        'present': present,
        'attendance_percentage': percentage
    })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
