import sqlite3
import sys


sys.stdout.reconfigure(encoding="utf-8")


def run_query(cursor, title, sql):
    print("=" * 80)
    print(title)
    print(sql.strip())
    print("-" * 80)

    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print()


def create_sample_data(cursor):
    cursor.executescript(
        """
        drop table if exists students;
        drop table if exists courses;

        create table courses (
            id integer primary key,
            course_name text not null
        );

        create table students (
            id integer primary key,
            name text not null,
            city text not null,
            score integer not null,
            course_id integer not null,
            foreign key (course_id) references courses(id)
        );

        insert into courses (id, course_name) values
            (1, 'Python'),
            (2, 'SQL'),
            (3, 'RAG');

        insert into students (id, name, city, score, course_id) values
            (1, 'Alice', 'Beijing', 95, 1),
            (2, 'Bob', 'Shanghai', 82, 2),
            (3, 'Cindy', 'Beijing', 88, 3),
            (4, 'David', 'Shenzhen', 76, 1),
            (5, 'Eva', 'Shanghai', 91, 3),
            (6, 'Frank', 'Beijing', 84, 2);
        """
    )


def main():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    create_sample_data(cursor)

    run_query(
        cursor,
        "1. select: 查询学生姓名和分数",
        """
        select name, score
        from students;
        """,
    )

    run_query(
        cursor,
        "2. where: 查询分数 >= 90 的学生",
        """
        select name, city, score
        from students
        where score >= 90;
        """,
    )

    run_query(
        cursor,
        "3. order by: 按分数从高到低排序",
        """
        select name, city, score
        from students
        order by score desc;
        """,
    )

    run_query(
        cursor,
        "4. group by: 按城市统计平均分",
        """
        select city, avg(score) as avg_score
        from students
        group by city;
        """,
    )

    run_query(
        cursor,
        "5. join: 查询学生和课程名称",
        """
        select students.name, courses.course_name, students.score
        from students
        join courses on students.course_id = courses.id;
        """,
    )

    run_query(
        cursor,
        "6. 手动练习参考：查询北京学生并按分数从高到低排序",
        """
        select name, city, score
        from students
        where city = 'Beijing'
        order by score desc;
        """,
    )

    run_query(
        cursor,
        "7. join + group by: 按课程统计平均分",
        """
        select courses.course_name, avg(students.score) as avg_score
        from students
        join courses on students.course_id = courses.id
        group by courses.course_name;
        """,
    )

    connection.close()


if __name__ == "__main__":
    main()

