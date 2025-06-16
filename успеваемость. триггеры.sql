SELECT * FROM classes;

-- Заполнение оценок для 1А класса
-- В 1 классе обычно используется безотметочная система в первом полугодии,
-- но для демонстрации добавим оценки за второе полугодие

-- Получаем ID учеников 1А класса и предметы, которые они изучают
-- Предметы для 1А класса: Математика (1), Русский язык (2), Литература (3), 
-- Английский язык (4), Физическая культура (5), Музыка (6), ИЗО (7), Окружающий мир (8), Технология (9)

-- Оценки за февраль 2025
INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id, comment) VALUES
-- Абрамов Артем (student_id = 1)
(1, 1, 5, '2025-02-03', 'устный ответ', 23, 'Отлично решает примеры'),
(1, 1, 4, '2025-02-10', 'самостоятельная', 23, NULL),
(1, 1, 5, '2025-02-17', 'домашнее задание', 23, NULL),
(1, 2, 4, '2025-02-04', 'письменная работа', 30, 'Хороший почерк'),
(1, 2, 4, '2025-02-11', 'устный ответ', 30, NULL),
(1, 2, 5, '2025-02-18', 'контрольная', 30, 'Без ошибок'),
(1, 3, 5, '2025-02-05', 'чтение', 31, 'Выразительное чтение'),
(1, 4, 4, '2025-02-06', 'устный ответ', 32, 'Good pronunciation'),
(1, 5, 5, '2025-02-07', 'нормативы', 35, 'Отличная физическая форма'),
(1, 8, 5, '2025-02-12', 'проект', 26, 'Интересная презентация о животных'),

-- Белкина Анна (student_id = 2)
(2, 1, 5, '2025-02-03', 'устный ответ', 23, 'Активна на уроке'),
(2, 1, 5, '2025-02-10', 'самостоятельная', 23, 'Все задания выполнены'),
(2, 1, 5, '2025-02-17', 'домашнее задание', 23, NULL),
(2, 2, 5, '2025-02-04', 'письменная работа', 30, 'Аккуратная работа'),
(2, 2, 5, '2025-02-11', 'устный ответ', 30, 'Знает все правила'),
(2, 2, 5, '2025-02-18', 'контрольная', 30, 'Отлично!'),
(2, 3, 5, '2025-02-05', 'чтение', 31, 'Читает бегло'),
(2, 4, 5, '2025-02-06', 'устный ответ', 32, 'Excellent!'),
(2, 6, 5, '2025-02-13', 'пение', 36, 'Чистое интонирование'),
(2, 7, 5, '2025-02-14', 'рисунок', 37, 'Творческий подход'),

-- Волков Максим (student_id = 3)
(3, 1, 4, '2025-02-03', 'устный ответ', 23, NULL),
(3, 1, 3, '2025-02-10', 'самостоятельная', 23, 'Нужно быть внимательнее'),
(3, 1, 4, '2025-02-17', 'домашнее задание', 23, 'Есть прогресс'),
(3, 2, 3, '2025-02-04', 'письменная работа', 30, 'Работаем над почерком'),
(3, 2, 4, '2025-02-11', 'устный ответ', 30, NULL),
(3, 2, 4, '2025-02-18', 'контрольная', 30, 'Хорошо'),
(3, 3, 4, '2025-02-05', 'чтение', 31, NULL),
(3, 5, 5, '2025-02-07', 'нормативы', 35, 'Спортивный мальчик'),
(3, 8, 4, '2025-02-12', 'устный ответ', 26, NULL),
(3, 9, 4, '2025-02-19', 'поделка', 38, 'Старательно работает'),

-- Гаврилова София (student_id = 4)
(4, 1, 5, '2025-02-03', 'устный ответ', 23, 'Умница!'),
(4, 1, 5, '2025-02-10', 'самостоятельная', 23, NULL),
(4, 1, 4, '2025-02-17', 'домашнее задание', 23, NULL),
(4, 2, 5, '2025-02-04', 'письменная работа', 30, 'Грамотно пишет'),
(4, 2, 5, '2025-02-11', 'устный ответ', 30, NULL),
(4, 2, 5, '2025-02-18', 'контрольная', 30, 'Молодец!'),
(4, 3, 5, '2025-02-05', 'чтение', 31, 'Отличная техника чтения'),
(4, 4, 5, '2025-02-06', 'устный ответ', 32, 'Very good!'),
(4, 6, 5, '2025-02-13', 'пение', 36, NULL),
(4, 7, 5, '2025-02-14', 'рисунок', 37, 'Художественные способности'),

-- Дмитриев Иван (student_id = 5)
(5, 1, 4, '2025-02-03', 'устный ответ', 23, NULL),
(5, 1, 4, '2025-02-10', 'самостоятельная', 23, NULL),
(5, 1, 5, '2025-02-17', 'домашнее задание', 23, 'Отличная работа'),
(5, 2, 4, '2025-02-04', 'письменная работа', 30, NULL),
(5, 2, 4, '2025-02-11', 'устный ответ', 30, NULL),
(5, 2, 4, '2025-02-18', 'контрольная', 30, 'Хорошо'),
(5, 3, 4, '2025-02-05', 'чтение', 31, NULL),
(5, 4, 4, '2025-02-06', 'устный ответ', 32, NULL),
(5, 5, 5, '2025-02-07', 'нормативы', 35, 'Активен на уроках'),
(5, 8, 4, '2025-02-12', 'устный ответ', 26, NULL),

-- Егорова Мария (student_id = 6)
(6, 1, 5, '2025-02-03', 'устный ответ', 23, 'Логическое мышление'),
(6, 1, 5, '2025-02-10', 'самостоятельная', 23, NULL),
(6, 1, 5, '2025-02-17', 'домашнее задание', 23, NULL),
(6, 2, 4, '2025-02-04', 'письменная работа', 30, NULL),
(6, 2, 5, '2025-02-11', 'устный ответ', 30, 'Богатый словарный запас'),
(6, 2, 5, '2025-02-18', 'контрольная', 30, NULL),
(6, 3, 5, '2025-02-05', 'чтение', 31, 'Понимает прочитанное'),
(6, 4, 4, '2025-02-06', 'устный ответ', 32, NULL),
(6, 6, 5, '2025-02-13', 'пение', 36, NULL),
(6, 8, 5, '2025-02-12', 'проект', 26, 'Исследовательские навыки'),

-- Жуков Даниил (student_id = 7)
(7, 1, 3, '2025-02-03', 'устный ответ', 23, 'Нужна помощь'),
(7, 1, 4, '2025-02-10', 'самостоятельная', 23, 'Прогресс'),
(7, 1, 4, '2025-02-17', 'домашнее задание', 23, NULL),
(7, 2, 3, '2025-02-04', 'письменная работа', 30, 'Больше практики'),
(7, 2, 3, '2025-02-11', 'устный ответ', 30, NULL),
(7, 2, 4, '2025-02-18', 'контрольная', 30, 'Улучшение'),
(7, 3, 4, '2025-02-05', 'чтение', 31, NULL),
(7, 5, 5, '2025-02-07', 'нормативы', 35, 'Хорошая физическая подготовка'),
(7, 8, 4, '2025-02-12', 'устный ответ', 26, NULL),
(7, 9, 5, '2025-02-19', 'поделка', 38, 'Золотые руки'),

-- Зайцева Алиса (student_id = 8)
(8, 1, 5, '2025-02-03', 'устный ответ', 23, NULL),
(8, 1, 4, '2025-02-10', 'самостоятельная', 23, NULL),
(8, 1, 5, '2025-02-17', 'домашнее задание', 23, NULL),
(8, 2, 5, '2025-02-04', 'письменная работа', 30, 'Каллиграфический почерк'),
(8, 2, 5, '2025-02-11', 'устный ответ', 30, NULL),
(8, 2, 5, '2025-02-18', 'контрольная', 30, NULL),
(8, 3, 5, '2025-02-05', 'чтение', 31, 'Артистичное чтение'),
(8, 4, 5, '2025-02-06', 'устный ответ', 32, 'Perfect!'),
(8, 7, 5, '2025-02-14', 'рисунок', 37, 'Талант к рисованию'),
(8, 8, 5, '2025-02-12', 'устный ответ', 26, NULL),

-- Иванов Егор (student_id = 9)
(9, 1, 4, '2025-02-03', 'устный ответ', 23, NULL),
(9, 1, 4, '2025-02-10', 'самостоятельная', 23, NULL),
(9, 1, 4, '2025-02-17', 'домашнее задание', 23, NULL),
(9, 2, 4, '2025-02-04', 'письменная работа', 30, NULL),
(9, 2, 4, '2025-02-11', 'устный ответ', 30, NULL),
(9, 2, 4, '2025-02-18', 'контрольная', 30, 'Стабильно хорошо'),
(9, 3, 4, '2025-02-05', 'чтение', 31, NULL),
(9, 4, 3, '2025-02-06', 'устный ответ', 32, 'Нужна практика'),
(9, 5, 4, '2025-02-07', 'нормативы', 35, NULL),
(9, 8, 4, '2025-02-12', 'устный ответ', 26, NULL),

-- Климова Василиса (student_id = 10)
(10, 1, 5, '2025-02-03', 'устный ответ', 23, 'Отличница'),
(10, 1, 5, '2025-02-10', 'самостоятельная', 23, NULL),
(10, 1, 5, '2025-02-17', 'домашнее задание', 23, NULL),
(10, 2, 5, '2025-02-04', 'письменная работа', 30, NULL),
(10, 2, 5, '2025-02-11', 'устный ответ', 30, NULL),
(10, 2, 5, '2025-02-18', 'контрольная', 30, 'Безупречно'),
(10, 3, 5, '2025-02-05', 'чтение', 31, NULL),
(10, 4, 5, '2025-02-06', 'устный ответ', 32, NULL),
(10, 6, 5, '2025-02-13', 'пение', 36, 'Музыкальный слух'),
(10, 7, 5, '2025-02-14', 'рисунок', 37, NULL);

-- Добавим оценки за март 2025 для разнообразия
INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id, comment) VALUES
-- Продолжим с остальными учениками класса
-- Лебедев Кирилл (student_id = 11)
(11, 1, 4, '2025-03-03', 'устный ответ', 23, NULL),
(11, 1, 5, '2025-03-10', 'контрольная', 23, 'Отличный результат'),
(11, 2, 4, '2025-03-04', 'письменная работа', 30, NULL),
(11, 2, 4, '2025-03-11', 'диктант', 30, '2 ошибки'),
(11, 3, 5, '2025-03-05', 'пересказ', 31, 'Подробный пересказ'),
(11, 4, 4, '2025-03-06', 'письменная работа', 32, NULL),
(11, 5, 5, '2025-03-07', 'нормативы', 35, NULL),
(11, 8, 5, '2025-03-12', 'проект', 26, 'Презентация о растениях'),

-- Морозова Полина (student_id = 12)
(12, 1, 5, '2025-03-03', 'устный ответ', 23, NULL),
(12, 1, 5, '2025-03-10', 'контрольная', 23, NULL),
(12, 2, 5, '2025-03-04', 'письменная работа', 30, 'Грамотно'),
(12, 2, 5, '2025-03-11', 'диктант', 30, 'Без ошибок'),
(12, 3, 5, '2025-03-05', 'чтение наизусть', 31, 'Выразительно'),
(12, 4, 5, '2025-03-06', 'диалог', 32, 'Great job!'),
(12, 6, 5, '2025-03-13', 'концерт', 36, 'Солистка хора'),
(12, 7, 5, '2025-03-14', 'выставка', 37, NULL),

-- Николаев Тимофей (student_id = 13)
(13, 1, 3, '2025-03-03', 'устный ответ', 23, 'Нужны дополнительные занятия'),
(13, 1, 4, '2025-03-10', 'контрольная', 23, 'Прогресс'),
(13, 2, 3, '2025-03-04', 'письменная работа', 30, 'Работаем над ошибками'),
(13, 2, 4, '2025-03-11', 'диктант', 30, NULL),
(13, 3, 4, '2025-03-05', 'чтение', 31, NULL),
(13, 5, 5, '2025-03-07', 'эстафета', 35, 'Быстрый'),
(13, 8, 4, '2025-03-12', 'устный ответ', 26, NULL),
(13, 9, 4, '2025-03-19', 'поделка', 38, NULL),

-- Орлова Елизавета (student_id = 14)
(14, 1, 5, '2025-03-03', 'устный ответ', 23, 'Всегда готова к уроку'),
(14, 1, 5, '2025-03-10', 'контрольная', 23, NULL),
(14, 2, 4, '2025-03-04', 'письменная работа', 30, NULL),
(14, 2, 5, '2025-03-11', 'диктант', 30, '1 ошибка'),
(14, 3, 5, '2025-03-05', 'чтение', 31, NULL),
(14, 4, 4, '2025-03-06', 'тест', 32, NULL),
(14, 6, 5, '2025-03-13', 'пение', 36, NULL),
(14, 8, 5, '2025-03-12', 'опыт', 26, 'Любознательная'),

-- Петров Александр (student_id = 15)
(15, 1, 4, '2025-03-03', 'устный ответ', 23, NULL),
(15, 1, 4, '2025-03-10', 'контрольная', 23, NULL),
(15, 2, 4, '2025-03-04', 'письменная работа', 30, NULL),
(15, 2, 4, '2025-03-11', 'диктант', 30, NULL),
(15, 3, 4, '2025-03-05', 'чтение', 31, NULL),
(15, 4, 4, '2025-03-06', 'устный ответ', 32, NULL),
(15, 5, 5, '2025-03-07', 'игра', 35, 'Командный игрок'),
(15, 9, 5, '2025-03-19', 'проект', 38, 'Конструктор'),

-- Романова Варвара (student_id = 16)
(16, 1, 5, '2025-03-03', 'устный ответ', 23, NULL),
(16, 1, 4, '2025-03-10', 'контрольная', 23, 'Небольшая ошибка'),
(16, 2, 5, '2025-03-04', 'письменная работа', 30, NULL),
(16, 2, 5, '2025-03-11', 'диктант', 30, NULL),
(16, 3, 5, '2025-03-05', 'чтение', 31, 'Читает с выражением'),
(16, 4, 5, '2025-03-06', 'презентация', 32, 'Creative!'),
(16, 7, 5, '2025-03-14', 'рисунок', 37, 'Чувство цвета'),
(16, 8, 5, '2025-03-12', 'наблюдение', 26, NULL),

-- Смирнов Михаил (student_id = 17)
(17, 1, 4, '2025-03-03', 'устный ответ', 23, NULL),
(17, 1, 4, '2025-03-10', 'контрольная', 23, NULL),
(17, 2, 3, '2025-03-04', 'письменная работа', 30, 'Неаккуратно'),
(17, 2, 4, '2025-03-11', 'диктант', 30, 'Старается'),
(17, 3, 4, '2025-03-05', 'чтение', 31, NULL),
(17, 5, 5, '2025-03-07', 'нормативы', 35, NULL),
(17, 8, 4, '2025-03-12', 'устный ответ', 26, NULL),
(17, 9, 4, '2025-03-19', 'поделка', 38, NULL),

-- Титова Ксения (student_id = 18)
(18, 1, 5, '2025-03-03', 'устный ответ', 23, 'Сообразительная'),
(18, 1, 5, '2025-03-10', 'контрольная', 23, NULL),
(18, 2, 5, '2025-03-04', 'письменная работа', 30, NULL),
(18, 2, 5, '2025-03-11', 'диктант', 30, NULL),
(18, 3, 5, '2025-03-05', 'чтение', 31, NULL),
(18, 4, 4, '2025-03-06', 'устный ответ', 32, NULL),
(18, 6, 5, '2025-03-13', 'пение', 36, 'Чисто поёт'),
(18, 7, 5, '2025-03-14', 'аппликация', 37, NULL),

-- Ушаков Владислав (student_id = 19)
(19, 1, 3, '2025-03-03', 'устный ответ', 23, 'Невнимателен'),
(19, 1, 4, '2025-03-10', 'контрольная', 23, 'Улучшение'),
(19, 2, 3, '2025-03-04', 'письменная работа', 30, NULL),
(19, 2, 3, '2025-03-11', 'диктант', 30, 'Много ошибок'),
(19, 3, 4, '2025-03-05', 'чтение', 31, NULL),
(19, 5, 5, '2025-03-07', 'нормативы', 35, 'Спортивный'),
(19, 8, 4, '2025-03-12', 'устный ответ', 26, NULL),
(19, 9, 5, '2025-03-19', 'модель', 38, 'Технические способности'),

-- Федорова Дарья (student_id = 20)
(20, 1, 5, '2025-03-03', 'устный ответ', 23, NULL),
(20, 1, 5, '2025-03-10', 'контрольная', 23, 'Отлично'),
(20, 2, 5, '2025-03-04', 'письменная работа', 30, NULL),
(20, 2, 5, '2025-03-11', 'диктант', 30, NULL),
(20, 3, 5, '2025-03-05', 'инсценировка', 31, 'Артистична'),
(20, 4, 5, '2025-03-06', 'песня', 32, 'Beautiful voice!'),
(20, 6, 5, '2025-03-13', 'выступление', 36, NULL),
(20, 8, 5, '2025-03-12', 'доклад', 26, NULL),

-- Добавим оценки за апрель для оставшихся учеников
-- Чернов Никита (student_id = 21)
(21, 1, 4, '2025-04-07', 'устный ответ', 23, NULL),
(21, 1, 4, '2025-04-14', 'самостоятельная', 23, NULL),
(21, 2, 4, '2025-04-08', 'изложение', 30, NULL),
(21, 2, 4, '2025-04-15', 'словарный диктант', 30, NULL),
(21, 3, 4, '2025-04-09', 'чтение', 31, NULL),
(21, 4, 3, '2025-04-10', 'устный ответ', 32, 'Shy student'),
(21, 5, 4, '2025-04-11', 'нормативы', 35, NULL),

-- Шишкина Арина (student_id = 22)
(22, 1, 5, '2025-04-07', 'устный ответ', 23, 'Активна'),
(22, 1, 5, '2025-04-14', 'контрольная', 23, NULL),
(22, 2, 5, '2025-04-08', 'сочинение', 30, 'Творческая работа'),
(22, 2, 5, '2025-04-15', 'тест', 30, NULL),
(22, 3, 5, '2025-04-09', 'чтение наизусть', 31, NULL),
(22, 4, 5, '2025-04-10', 'проект', 32, 'Excellent presentation!'),
(22, 7, 5, '2025-04-16', 'выставка работ', 37, 'Лучшая работа'),

-- Яковлев Глеб (student_id = 23)
(23, 1, 4, '2025-04-07', 'устный ответ', 23, NULL),
(23, 1, 3, '2025-04-14', 'контрольная', 23, 'Нужна помощь'),
(23, 2, 4, '2025-04-08', 'письменная работа', 30, NULL),
(23, 2, 4, '2025-04-15', 'диктант', 30, NULL),
(23, 3, 4, '2025-04-09', 'чтение', 31, NULL),
(23, 5, 5, '2025-04-11', 'соревнования', 35, '1 место в беге'),
(23, 8, 4, '2025-04-17', 'тест', 26, NULL),

-- Антонова Милана (student_id = 24)
(24, 1, 5, '2025-04-07', 'устный ответ', 23, NULL),
(24, 1, 5, '2025-04-14', 'олимпиада', 23, 'Призёр'),
(24, 2, 5, '2025-04-08', 'письменная работа', 30, NULL),
(24, 2, 5, '2025-04-15', 'диктант', 30, NULL),
(24, 3, 5, '2025-04-09', 'конкурс чтецов', 31, '1 место'),
(24, 4, 5, '2025-04-10', 'устный ответ', 32, NULL),
(24, 6, 5, '2025-04-18', 'концерт', 36, 'Солистка'),

-- Борисов Роман (student_id = 25)
(25, 1, 4, '2025-04-07', 'устный ответ', 23, NULL),
(25, 1, 4, '2025-04-14', 'самостоятельная', 23, NULL),
(25, 2, 4, '2025-04-08', 'письменная работа', 30, NULL),
(25, 2, 4, '2025-04-15', 'диктант', 30, NULL),
(25, 3, 4, '2025-04-09', 'чтение', 31, NULL),
(25, 5, 4, '2025-04-11', 'нормативы', 35, NULL),
(25, 9, 5, '2025-04-19', 'изделие', 38, 'Аккуратная работа');

INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id, comment) VALUES
-- Виноградова Ева (student_id = 26)
(26, 1, 5, '2025-04-07', 'устный ответ', 23, 'Отличные знания'),
(26, 1, 5, '2025-04-14', 'контрольная', 23, NULL),
(26, 2, 5, '2025-04-08', 'письменная работа', 30, 'Безупречно'),
(26, 2, 5, '2025-04-15', 'диктант', 30, NULL),
(26, 3, 5, '2025-04-09', 'чтение', 31, 'Выразительно'),
(26, 4, 5, '2025-04-10', 'диалог', 32, 'Perfect!'),
(26, 7, 5, '2025-04-16', 'рисунок', 37, 'Художественный талант'),
(26, 8, 5, '2025-04-17', 'исследование', 26, NULL),

-- Герасимов Матвей (student_id = 27)
(27, 1, 3, '2025-04-07', 'устный ответ', 23, 'Отвлекается'),
(27, 1, 4, '2025-04-14', 'самостоятельная', 23, 'Есть улучшения'),
(27, 2, 3, '2025-04-08', 'письменная работа', 30, 'Неаккуратно'),
(27, 2, 4, '2025-04-15', 'диктант', 30, 'Прогресс'),
(27, 3, 4, '2025-04-09', 'чтение', 31, NULL),
(27, 5, 5, '2025-04-11', 'эстафета', 35, 'Быстрый и ловкий'),
(27, 8, 4, '2025-04-17', 'устный ответ', 26, NULL),
(27, 9, 4, '2025-04-19', 'поделка', 38, NULL),

-- Денисова Стефания (student_id = 28)
(28, 1, 5, '2025-04-07', 'устный ответ', 23, 'Умница!'),
(28, 1, 5, '2025-04-14', 'контрольная', 23, '100%'),
(28, 2, 5, '2025-04-08', 'письменная работа', 30, 'Образцовая работа'),
(28, 2, 5, '2025-04-15', 'диктант', 30, 'Без ошибок'),
(28, 3, 5, '2025-04-09', 'инсценировка', 31, 'Талантливая актриса'),
(28, 4, 5, '2025-04-10', 'презентация', 32, 'Outstanding!'),
(28, 6, 5, '2025-04-18', 'выступление', 36, 'Прекрасный голос'),
(28, 7, 5, '2025-04-16', 'проект', 37, 'Креативность');




-- Добавим итоговые оценки за четверть (май 2025) для всех учеников 1А класса
INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id, comment) VALUES
-- Итоговые контрольные работы за 4 четверть
(1, 1, 5, '2025-05-15', 'итоговая контрольная', 23, 'Отличный результат за год'),
(1, 2, 4, '2025-05-16', 'итоговая контрольная', 30, 'Хорошие знания'),
(1, 3, 5, '2025-05-17', 'техника чтения', 31, 'Норма превышена'),
(1, 4, 4, '2025-05-18', 'итоговый тест', 32, 'Good progress'),

(2, 1, 5, '2025-05-15', 'итоговая контрольная', 23, 'Отличница'),
(2, 2, 5, '2025-05-16', 'итоговая контрольная', 30, 'Превосходно'),
(2, 3, 5, '2025-05-17', 'техника чтения', 31, 'Лучший результат в классе'),
(2, 4, 5, '2025-05-18', 'итоговый тест', 32, 'Excellent!'),

(3, 1, 4, '2025-05-15', 'итоговая контрольная', 23, 'Хороший результат'),
(3, 2, 4, '2025-05-16', 'итоговая контрольная', 30, 'Есть прогресс'),
(3, 3, 4, '2025-05-17', 'техника чтения', 31, 'Норма'),
(3, 4, 3, '2025-05-18', 'итоговый тест', 32, 'Needs practice'),

(4, 1, 5, '2025-05-15', 'итоговая контрольная', 23, 'Молодец!'),
(4, 2, 5, '2025-05-16', 'итоговая контрольная', 30, 'Отлично'),
(4, 3, 5, '2025-05-17', 'техника чтения', 31, 'Выше нормы'),
(4, 4, 5, '2025-05-18', 'итоговый тест', 32, 'Very good!'),

(5, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(5, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(5, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(5, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(6, 1, 5, '2025-05-15', 'итоговая контрольная', 23, 'Отличный результат'),
(6, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(6, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(6, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(7, 1, 4, '2025-05-15', 'итоговая контрольная', 23, 'Справился'),
(7, 2, 4, '2025-05-16', 'итоговая контрольная', 30, 'Улучшил результат'),
(7, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(7, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(8, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(8, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(8, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(8, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(9, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(9, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(9, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(9, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(10, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(10, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(10, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(10, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(11, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(11, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(11, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(11, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(12, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(12, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(12, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(12, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(13, 1, 4, '2025-05-15', 'итоговая контрольная', 23, 'Переведён во 2 класс'),
(13, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(13, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(13, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(14, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(14, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(14, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(14, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(15, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(15, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(15, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(15, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(16, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(16, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(16, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(16, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(17, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(17, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(17, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(17, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(18, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(18, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(18, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(18, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(19, 1, 4, '2025-05-15', 'итоговая контрольная', 23, 'Рекомендованы летние занятия'),
(19, 2, 3, '2025-05-16', 'итоговая контрольная', 30, 'Нужна помощь летом'),
(19, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(19, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(20, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(20, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(20, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(20, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(21, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(21, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(21, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(21, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(22, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(22, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(22, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(22, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(23, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(23, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(23, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(23, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(24, 1, 5, '2025-05-15', 'итоговая контрольная', 23, 'Похвальный лист'),
(24, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(24, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(24, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(25, 1, 4, '2025-05-15', 'итоговая контрольная', 23, NULL),
(25, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(25, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(25, 4, 4, '2025-05-18', 'итоговый тест', 32, NULL),

(26, 1, 5, '2025-05-15', 'итоговая контрольная', 23, NULL),
(26, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(26, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(26, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL),

(27, 1, 4, '2025-05-15', 'итоговая контрольная', 23, 'Успешно окончил 1 класс'),
(27, 2, 4, '2025-05-16', 'итоговая контрольная', 30, NULL),
(27, 3, 4, '2025-05-17', 'техника чтения', 31, NULL),
(27, 4, 3, '2025-05-18', 'итоговый тест', 32, NULL),

(28, 1, 5, '2025-05-15', 'итоговая контрольная', 23, 'Отличница, похвальный лист'),
(28, 2, 5, '2025-05-16', 'итоговая контрольная', 30, NULL),
(28, 3, 5, '2025-05-17', 'техника чтения', 31, NULL),
(28, 4, 5, '2025-05-18', 'итоговый тест', 32, NULL);




SELECT * FROM grades;

SELECT * FROM student_progress;




-- Функция для пересчета среднего балла и обновления student_progress
CREATE OR REPLACE FUNCTION update_student_progress()
RETURNS TRIGGER AS $$
DECLARE
    v_average_grade NUMERIC(3,2);
    v_final_grade INTEGER;
    v_period_type VARCHAR(20);
    v_period_number INTEGER;
    v_academic_year VARCHAR(9);
    v_student_id INTEGER;
    v_subject_id INTEGER;
BEGIN
    -- Определяем student_id и subject_id в зависимости от операции
    IF TG_OP = 'DELETE' THEN
        v_student_id := OLD.student_id;
        v_subject_id := OLD.subject_id;
    ELSE
        v_student_id := NEW.student_id;
        v_subject_id := NEW.subject_id;
    END IF;
    
    -- Определяем период и учебный год на основе даты оценки
    -- Для примера используем текущую дату для определения периода
    IF TG_OP = 'DELETE' THEN
        v_academic_year := CASE 
            WHEN EXTRACT(MONTH FROM OLD.grade_date) >= 9 THEN 
                EXTRACT(YEAR FROM OLD.grade_date) || '-' || (EXTRACT(YEAR FROM OLD.grade_date) + 1)
            ELSE 
                (EXTRACT(YEAR FROM OLD.grade_date) - 1) || '-' || EXTRACT(YEAR FROM OLD.grade_date)
        END;
    ELSE
        v_academic_year := CASE 
            WHEN EXTRACT(MONTH FROM NEW.grade_date) >= 9 THEN 
                EXTRACT(YEAR FROM NEW.grade_date) || '-' || (EXTRACT(YEAR FROM NEW.grade_date) + 1)
            ELSE 
                (EXTRACT(YEAR FROM NEW.grade_date) - 1) || '-' || EXTRACT(YEAR FROM NEW.grade_date)
        END;
    END IF;
    
    -- Рассчитываем средний балл за год
    SELECT 
        AVG(grade)::NUMERIC(3,2),
        ROUND(AVG(grade))::INTEGER
    INTO 
        v_average_grade,
        v_final_grade
    FROM grades
    WHERE student_id = v_student_id 
        AND subject_id = v_subject_id
        AND grade_date >= CASE 
            WHEN SUBSTRING(v_academic_year, 1, 4)::INTEGER = EXTRACT(YEAR FROM CURRENT_DATE) 
                AND EXTRACT(MONTH FROM CURRENT_DATE) < 9 
            THEN (SUBSTRING(v_academic_year, 1, 4)::INTEGER - 1) || '-09-01'
            ELSE SUBSTRING(v_academic_year, 1, 4) || '-09-01'
        END::DATE
        AND grade_date <= CASE 
            WHEN SUBSTRING(v_academic_year, 1, 4)::INTEGER = EXTRACT(YEAR FROM CURRENT_DATE) 
                AND EXTRACT(MONTH FROM CURRENT_DATE) < 9 
            THEN SUBSTRING(v_academic_year, 1, 4) || '-05-31'
            ELSE SUBSTRING(v_academic_year, 6, 4) || '-05-31'
        END::DATE;
    
    -- Если есть оценки, обновляем или вставляем запись
    IF v_average_grade IS NOT NULL THEN
        -- Обновляем запись за год
        INSERT INTO student_progress (
            student_id, 
            subject_id, 
            period_type, 
            period_number, 
            academic_year, 
            average_grade, 
            final_grade
        ) VALUES (
            v_student_id,
            v_subject_id,
            'год',
            NULL,
            v_academic_year,
            v_average_grade,
            v_final_grade
        )
        ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
        DO UPDATE SET
            average_grade = EXCLUDED.average_grade,
            final_grade = EXCLUDED.final_grade;
        
        -- Также обновляем четвертные оценки
        -- 1 четверть (сентябрь-октябрь)
        SELECT 
            AVG(grade)::NUMERIC(3,2),
            ROUND(AVG(grade))::INTEGER
        INTO 
            v_average_grade,
            v_final_grade
        FROM grades
        WHERE student_id = v_student_id 
            AND subject_id = v_subject_id
            AND grade_date >= (SUBSTRING(v_academic_year, 1, 4) || '-09-01')::DATE
            AND grade_date <= (SUBSTRING(v_academic_year, 1, 4) || '-10-31')::DATE;
            
        IF v_average_grade IS NOT NULL THEN
            INSERT INTO student_progress (
                student_id, subject_id, period_type, period_number, 
                academic_year, average_grade, final_grade
            ) VALUES (
                v_student_id, v_subject_id, 'четверть', 1, 
                v_academic_year, v_average_grade, v_final_grade
            )
            ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
            DO UPDATE SET
                average_grade = EXCLUDED.average_grade,
                final_grade = EXCLUDED.final_grade;
        END IF;
        
        -- 2 четверть (ноябрь-декабрь)
        SELECT 
            AVG(grade)::NUMERIC(3,2),
            ROUND(AVG(grade))::INTEGER
        INTO 
            v_average_grade,
            v_final_grade
        FROM grades
        WHERE student_id = v_student_id 
            AND subject_id = v_subject_id
            AND grade_date >= (SUBSTRING(v_academic_year, 1, 4) || '-11-01')::DATE
            AND grade_date <= (SUBSTRING(v_academic_year, 1, 4) || '-12-31')::DATE;
            
        IF v_average_grade IS NOT NULL THEN
            INSERT INTO student_progress (
                student_id, subject_id, period_type, period_number, 
                academic_year, average_grade, final_grade
            ) VALUES (
                v_student_id, v_subject_id, 'четверть', 2, 
                v_academic_year, v_average_grade, v_final_grade
            )
            ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
            DO UPDATE SET
                average_grade = EXCLUDED.average_grade,
                final_grade = EXCLUDED.final_grade;
        END IF;
        
        -- 3 четверть (январь-март)
        SELECT 
            AVG(grade)::NUMERIC(3,2),
            ROUND(AVG(grade))::INTEGER
        INTO 
            v_average_grade,
            v_final_grade
        FROM grades
        WHERE student_id = v_student_id 
            AND subject_id = v_subject_id
            AND grade_date >= (SUBSTRING(v_academic_year, 6, 4) || '-01-01')::DATE
            AND grade_date <= (SUBSTRING(v_academic_year, 6, 4) || '-03-31')::DATE;
            
        IF v_average_grade IS NOT NULL THEN
            INSERT INTO student_progress (
                student_id, subject_id, period_type, period_number, 
                academic_year, average_grade, final_grade
            ) VALUES (
                v_student_id, v_subject_id, 'четверть', 3, 
                v_academic_year, v_average_grade, v_final_grade
            )
            ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
            DO UPDATE SET
                average_grade = EXCLUDED.average_grade,
                final_grade = EXCLUDED.final_grade;
        END IF;
        
        -- 4 четверть (апрель-май)
        SELECT 
            AVG(grade)::NUMERIC(3,2),
            ROUND(AVG(grade))::INTEGER
        INTO 
            v_average_grade,
            v_final_grade
        FROM grades
        WHERE student_id = v_student_id 
            AND subject_id = v_subject_id
            AND grade_date >= (SUBSTRING(v_academic_year, 6, 4) || '-04-01')::DATE
            AND grade_date <= (SUBSTRING(v_academic_year, 6, 4) || '-05-31')::DATE;
            
        IF v_average_grade IS NOT NULL THEN
            INSERT INTO student_progress (
                student_id, subject_id, period_type, period_number, 
                academic_year, average_grade, final_grade
            ) VALUES (
                v_student_id, v_subject_id, 'четверть', 4, 
                v_academic_year, v_average_grade, v_final_grade
            )
            ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
            DO UPDATE SET
                average_grade = EXCLUDED.average_grade,
                final_grade = EXCLUDED.final_grade;
        END IF;
        
        -- Полугодия для старших классов (проверяем, если ученик в 10-11 классе)
        IF EXISTS (
            SELECT 1 FROM students s 
            JOIN classes c ON s.class_id = c.class_id 
            WHERE s.student_id = v_student_id 
            AND c.class_number IN ('10А', '10Б', '11А', '11Б')
        ) THEN
            -- 1 полугодие
            SELECT 
                AVG(grade)::NUMERIC(3,2),
                ROUND(AVG(grade))::INTEGER
            INTO 
                v_average_grade,
                v_final_grade
            FROM grades
            WHERE student_id = v_student_id 
                AND subject_id = v_subject_id
                AND grade_date >= (SUBSTRING(v_academic_year, 1, 4) || '-09-01')::DATE
                AND grade_date <= (SUBSTRING(v_academic_year, 1, 4) || '-12-31')::DATE;
                
            IF v_average_grade IS NOT NULL THEN
                INSERT INTO student_progress (
                    student_id, subject_id, period_type, period_number, 
                    academic_year, average_grade, final_grade
                ) VALUES (
                    v_student_id, v_subject_id, 'полугодие', 1, 
                    v_academic_year, v_average_grade, v_final_grade
                )
                ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
                DO UPDATE SET
                    average_grade = EXCLUDED.average_grade,
                    final_grade = EXCLUDED.final_grade;
            END IF;
            
            -- 2 полугодие
            SELECT 
                AVG(grade)::NUMERIC(3,2),
                ROUND(AVG(grade))::INTEGER
            INTO 
                v_average_grade,
                v_final_grade
            FROM grades
            WHERE student_id = v_student_id 
                AND subject_id = v_subject_id
                AND grade_date >= (SUBSTRING(v_academic_year, 6, 4) || '-01-01')::DATE
                AND grade_date <= (SUBSTRING(v_academic_year, 6, 4) || '-05-31')::DATE;
                
            IF v_average_grade IS NOT NULL THEN
                INSERT INTO student_progress (
                    student_id, subject_id, period_type, period_number, 
                    academic_year, average_grade, final_grade
                ) VALUES (
                    v_student_id, v_subject_id, 'полугодие', 2, 
                    v_academic_year, v_average_grade, v_final_grade
                )
                ON CONFLICT (student_id, subject_id, period_type, period_number, academic_year) 
                DO UPDATE SET
                    average_grade = EXCLUDED.average_grade,
                    final_grade = EXCLUDED.final_grade;
            END IF;
        END IF;
    ELSE
        -- Если оценок больше нет, удаляем записи из student_progress
        DELETE FROM student_progress 
        WHERE student_id = v_student_id 
            AND subject_id = v_subject_id 
            AND academic_year = v_academic_year;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггеры для таблицы grades
DROP TRIGGER IF EXISTS trg_grades_insert_update_progress ON grades;
CREATE TRIGGER trg_grades_insert_update_progress
AFTER INSERT OR UPDATE ON grades
FOR EACH ROW
EXECUTE FUNCTION update_student_progress();

DROP TRIGGER IF EXISTS trg_grades_delete_update_progress ON grades;
CREATE TRIGGER trg_grades_delete_update_progress
AFTER DELETE ON grades
FOR EACH ROW
EXECUTE FUNCTION update_student_progress();

-- Функция для первоначального заполнения student_progress на основе существующих оценок
CREATE OR REPLACE FUNCTION fill_student_progress_from_existing_grades()
RETURNS void AS $$
DECLARE
    rec RECORD;
BEGIN
    -- Очищаем таблицу student_progress перед заполнением
    TRUNCATE TABLE student_progress;
    
    -- Получаем все уникальные комбинации student_id, subject_id, academic_year
    FOR rec IN 
        SELECT DISTINCT 
            g.student_id,
            g.subject_id,
            CASE 
                WHEN EXTRACT(MONTH FROM g.grade_date) >= 9 THEN 
                    EXTRACT(YEAR FROM g.grade_date) || '-' || (EXTRACT(YEAR FROM g.grade_date) + 1)
                ELSE 
                    (EXTRACT(YEAR FROM g.grade_date) - 1) || '-' || EXTRACT(YEAR FROM g.grade_date)
            END as academic_year
        FROM grades g
    LOOP
        -- Для каждой комбинации вызываем пересчет
        -- Создаем фиктивную операцию UPDATE для запуска триггера
        UPDATE grades 
        SET grade = grade 
        WHERE student_id = rec.student_id 
            AND subject_id = rec.subject_id
            AND grade_date = (
                SELECT MIN(grade_date) 
                FROM grades 
                WHERE student_id = rec.student_id 
                    AND subject_id = rec.subject_id
            );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Вызываем функцию для заполнения student_progress на основе существующих данных
SELECT fill_student_progress_from_existing_grades();

-- Проверяем результат
SELECT 
    sp.*,
    s.last_name || ' ' || s.first_name as student_name,
    sub.subject_name
FROM student_progress sp
JOIN students s ON sp.student_id = s.student_id
JOIN subjects sub ON sp.subject_id = sub.subject_id
WHERE s.class_id = 1 -- 1А класс
ORDER BY s.last_name, s.first_name, sub.subject_name, sp.period_type, sp.period_number
LIMIT 20;



SELECT * FROM students;
SELECT * FROM classes;
SELECT * FROM teachers;
SELECT * FROM subjects;
SELECT * FROM lessons;
SELECT * FROM grades;
SELECT * FROM student_progress;




-- Функция для каскадного удаления данных студента и обновления количества учеников в классе
CREATE OR REPLACE FUNCTION cascade_delete_student_data()
RETURNS TRIGGER AS $$
DECLARE
    v_class_id INTEGER;
BEGIN
    -- Сохраняем class_id удаляемого студента
    v_class_id := OLD.class_id;
    
    -- Удаляем все оценки студента
    DELETE FROM grades WHERE student_id = OLD.student_id;
    
    -- Удаляем все итоговые оценки студента
    DELETE FROM student_progress WHERE student_id = OLD.student_id;
    
    -- Обновляем количество учеников в классе (уменьшаем на 1)
    IF v_class_id IS NOT NULL THEN
        UPDATE classes 
        SET student_count = student_count - 1
        WHERE class_id = v_class_id
        AND student_count > 0; -- защита от отрицательных значений
    END IF;
    
    -- Логирование удаления (опционально)
    RAISE NOTICE 'Удален студент ID: %, из класса ID: %. Все связанные данные удалены.', 
                 OLD.student_id, v_class_id;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер BEFORE DELETE для каскадного удаления
DROP TRIGGER IF EXISTS trg_before_delete_student ON students;
CREATE TRIGGER trg_before_delete_student
BEFORE DELETE ON students
FOR EACH ROW
EXECUTE FUNCTION cascade_delete_student_data();

-- Функция для обновления количества учеников при добавлении студента
CREATE OR REPLACE FUNCTION update_student_count_on_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Увеличиваем количество учеников в классе при добавлении
    IF NEW.class_id IS NOT NULL THEN
        UPDATE classes 
        SET student_count = student_count + 1
        WHERE class_id = NEW.class_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для увеличения количества учеников при добавлении
DROP TRIGGER IF EXISTS trg_after_insert_student ON students;
CREATE TRIGGER trg_after_insert_student
AFTER INSERT ON students
FOR EACH ROW
EXECUTE FUNCTION update_student_count_on_insert();

-- Функция для обновления количества учеников при переводе в другой класс
CREATE OR REPLACE FUNCTION update_student_count_on_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Если студент переведен в другой класс
    IF OLD.class_id IS DISTINCT FROM NEW.class_id THEN
        -- Уменьшаем количество в старом классе
        IF OLD.class_id IS NOT NULL THEN
            UPDATE classes 
            SET student_count = student_count - 1
            WHERE class_id = OLD.class_id
            AND student_count > 0;
        END IF;
        
        -- Увеличиваем количество в новом классе
        IF NEW.class_id IS NOT NULL THEN
            UPDATE classes 
            SET student_count = student_count + 1
            WHERE class_id = NEW.class_id;
        END IF;
        
        RAISE NOTICE 'Студент ID: % переведен из класса ID: % в класс ID: %', 
                     NEW.student_id, OLD.class_id, NEW.class_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для обновления количества учеников при переводе
DROP TRIGGER IF EXISTS trg_after_update_student ON students;
CREATE TRIGGER trg_after_update_student
AFTER UPDATE ON students
FOR EACH ROW
EXECUTE FUNCTION update_student_count_on_update();

-- Функция для пересчета количества учеников в классе (для исправления рассинхронизации)
CREATE OR REPLACE FUNCTION recalculate_class_student_count(p_class_id INTEGER DEFAULT NULL)
RETURNS void AS $$
BEGIN
    IF p_class_id IS NULL THEN
        -- Пересчитываем для всех классов
        UPDATE classes c
        SET student_count = (
            SELECT COUNT(*)
            FROM students s
            WHERE s.class_id = c.class_id
        );
        RAISE NOTICE 'Количество учеников пересчитано для всех классов';
    ELSE
        -- Пересчитываем для конкретного класса
        UPDATE classes
        SET student_count = (
            SELECT COUNT(*)
            FROM students
            WHERE class_id = p_class_id
        )
        WHERE class_id = p_class_id;
        RAISE NOTICE 'Количество учеников пересчитано для класса ID: %', p_class_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Создаем представление для удобного просмотра информации о классах
CREATE OR REPLACE VIEW v_class_statistics AS
SELECT 
    c.class_id,
    c.class_number,
    c.student_count as registered_count,
    COUNT(s.student_id) as actual_count,
    CASE 
        WHEN c.student_count = COUNT(s.student_id) THEN 'Синхронизировано'
        ELSE 'Требуется пересчет'
    END as sync_status,
    t.last_name || ' ' || t.first_name || ' ' || COALESCE(t.middle_name, '') as homeroom_teacher
FROM classes c
LEFT JOIN students s ON c.class_id = s.class_id
LEFT JOIN teachers t ON c.homeroom_teacher_id = t.teacher_id
GROUP BY c.class_id, c.class_number, c.student_count, c.classroom, 
         t.last_name, t.first_name, t.middle_name
ORDER BY c.class_number;

-- Тестовые запросы для проверки работы триггеров
-- 1. Проверяем текущее состояние
SELECT * FROM v_class_statistics WHERE class_number = '1А';

-- 2. Пример удаления студента (закомментирован для безопасности)
-- DELETE FROM students WHERE student_id = 1;

-- 3. Пример добавления нового студента
-- INSERT INTO students (last_name, first_name, middle_name, birth_date, gender, class_id) 
-- VALUES ('Тестов', 'Тест', 'Тестович', '2018-01-01', 'М', 1);

-- 4. Пример перевода студента в другой класс
-- UPDATE students SET class_id = 2 WHERE student_id = 5;

-- 5. Функция для проверки целостности данных
CREATE OR REPLACE FUNCTION check_data_integrity()
RETURNS TABLE(
    check_type VARCHAR(100),
    status VARCHAR(50),
    details TEXT
) AS $$
BEGIN
    -- Проверка синхронизации количества учеников
    RETURN QUERY
    SELECT 
        'Синхронизация количества учеников'::VARCHAR(100),
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM v_class_statistics 
                WHERE sync_status = 'Требуется пересчет'
            ) THEN 'ОШИБКА'::VARCHAR(50)
            ELSE 'ОК'::VARCHAR(50)
        END,
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM v_class_statistics 
                WHERE sync_status = 'Требуется пересчет'
            ) THEN 
                'Классы с рассинхронизацией: ' || 
                string_agg(class_number, ', ' ORDER BY class_number)
            ELSE 'Все классы синхронизированы'
        END::TEXT
    FROM v_class_statistics
    WHERE sync_status = 'Требуется пересчет';
    
    -- Проверка студентов без класса
    RETURN QUERY
    SELECT 
        'Студенты без класса'::VARCHAR(100),
        CASE 
            WHEN COUNT(*) > 0 THEN 'ВНИМАНИЕ'::VARCHAR(50)
            ELSE 'ОК'::VARCHAR(50)
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 
                'Количество студентов без класса: ' || COUNT(*)::TEXT
            ELSE 'Все студенты распределены по классам'
        END::TEXT
    FROM students
    WHERE class_id IS NULL;
    
    -- Проверка оценок без студентов
    RETURN QUERY
    SELECT 
        'Оценки без студентов'::VARCHAR(100),
        CASE 
            WHEN COUNT(*) > 0 THEN 'ОШИБКА'::VARCHAR(50)
            ELSE 'ОК'::VARCHAR(50)
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 
                'Количество оценок-сирот: ' || COUNT(*)::TEXT
            ELSE 'Все оценки связаны со студентами'
        END::TEXT
    FROM grades g
    WHERE NOT EXISTS (
        SELECT 1 FROM students s 
        WHERE s.student_id = g.student_id
    );
    
    -- Проверка итоговых оценок без студентов
    RETURN QUERY
    SELECT 
        'Итоговые оценки без студентов'::VARCHAR(100),
        CASE 
            WHEN COUNT(*) > 0 THEN 'ОШИБКА'::VARCHAR(50)
            ELSE 'ОК'::VARCHAR(50)
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 
                'Количество итоговых оценок-сирот: ' || COUNT(*)::TEXT
            ELSE 'Все итоговые оценки связаны со студентами'
        END::TEXT
    FROM student_progress sp
    WHERE NOT EXISTS (
        SELECT 1 FROM students s 
        WHERE s.student_id = sp.student_id
    );
END;
$$ LANGUAGE plpgsql;

-- Выполняем проверку целостности данных
SELECT * FROM check_data_integrity();

-- Если нужно исправить рассинхронизацию, выполните:
SELECT recalculate_class_student_count();


