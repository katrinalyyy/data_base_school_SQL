SELECT * FROM students WHERE last_name = 'Родионова';
SELECT * FROM classes;
SELECT * FROM teachers;
SELECT * FROM subjects;
SELECT * FROM lessons;
SELECT * FROM grades ORDER BY grade_date;
SELECT DISTINCT * FROM student_progress ORDER BY student_id;
SELECT DISTINCT student_id, subject_id, period_time, period_number, academic_year FROM student_progress;

SELECT DISTINCT ON (student_id, subject_id)
    *
FROM student_progress
ORDER BY student_id, subject_id, progress_id DESC;


INSERT INTO classes (class_number, student_count, classroom, homeroom_teacher_id) VALUES
('11Г', 3, 315, 22); 

INSERT INTO students (last_name, first_name, middle_name, birth_date, gender, class_id) VALUES
('Тестовый1', 'Тест1','Тестович1', '2008-08-06', 'М', 23),
('Тестовый2', 'Тест2','Тестович2', '2008-08-06', 'М', 23),
('Тестовый3', 'Тест3','Тестович3', '2008-08-06', 'М', 23); 


UPDATE classes
SET student_count = 3
WHERE class_id = 23;


INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id) VALUES
(727, 1, 4, '2025-04-09', 'test', 31),
(727, 1, 2, '2025-04-09', 'test', 31),
(727, 1, 2, '2025-04-09', 'test', 31),
(727, 1, 3, '2025-04-09', 'test', 31),
(727, 1, 2, '2025-04-09', 'test', 31),
(727, 2, 4, '2025-04-09', 'test', 31),
(727, 2, 3, '2025-04-09', 'test', 31),

(728, 1, 3, '2008-04-09', 'test', 31),
(728, 2, 3, '2008-04-09', 'test', 31),
(728, 3, 3, '2008-04-09', 'test', 31),
(728, 2, 4, '2008-04-09', 'test', 31),
(728, 2, 5, '2008-04-09', 'test', 31),

(729, 1, 2, '2008-04-09', 'test', 31),
(729, 1, 4, '2008-04-09', 'test', 31); 


INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id) VALUES
(727, 1, 4, '2025-04-09', 'test', 31);

DELETE FROM grades
WHERE grade_id = 433;


DELETE FROM students WHERE student_id = 727;