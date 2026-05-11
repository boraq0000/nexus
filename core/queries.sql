--CREATE USER
INSERT INTO Users(name, email, password) VALUES ('nex', 'nex@gmail.com', '123nex')

--SIGN IN 
SELECT * FROM Users 
WHERE email= 'nex@gmail.com' AND password = '123nex' ;

--Display profile
SELECT user_id, Users.name, email, role, acadimic_year, subscription_type, points FROM Users
WHERE user_id = 001;   

--User Evaluations
SELECT project_id, project_title, feedback, score FROM evaluetions
JOIN projects ON projects.project_id = evaluations.project_id
WHERE user_id = 001;

--CREATE PROJECT
WITH new_project AS ( INSERT INTO projects(title, description, owner_id) VALUES ('Project 1', 'Description of Project 1', 001) RETURNING id )
INSERT INTO project_members(project_id, user_id, role)
SELECT id, 001, 'owner' FROM new_project
UNION
SELECT id, 002, 'member' FROM new_project
UNION
SELECT id, 003, 'member' FROM new_project;

--STUDENT PROJECTS
SELECT title FROM projects WHERE owner_id = 001
UNION
SELECT project.title FROM projects
JOIN project_members ON project.id = project_members.project_id
WHERE project_members.user_id = 001;

--PROJECT MEMBERS
SELECT user.name,user.id, 'owner' AS role FROM projects
JOIN Users ON Users.id = projects.owner_id
WHERE project_members.project.id = 001
UNION
SELECT user.name, user_id, 'member'AS role FROM projects
JOIN Users ON Users.id = project_members.user_id
WHERE project_members.project_id = 001;

--ADD MEMBER TO PROJECT
ALTER TABLE project_members ADD UNIQUE (user_id, project_id, email);
INSERT INTO project_members (user_id, name, email, project_id) VALUES (001, nex, nex@gmail.com, 001);

--DELETE MEMBER FROM PROJECT
/*DELETE FROM project_member WHERE USING Users
WHERE project.user_id = user_id AND Users.email = 'nex@gmail.com';*/
DELETE FROM project_members
WHERE user_id IN (SELECT id FROM Users WHERE email = 'nex@gmail.com');

--VIEW MEMBERS
SELECT user_id, user.name, user.email FROM Users 
JOIN project_members ON user_id = project_members.user_id
WHERE project_member.project_id = 001;

--DISPLAY PROJECT INFO
SELECT project_id, project_title, project.description, user.name, email, COUNT(user_id) AS members_count 
FROM projects
LEFT JOIN project_members ON project_members.project_id = projects.project_id
LEFT JOIN users ON user_id = project_members.project_id
WHERE project_id = 001
GROUP BY project_id, user_id;

--create evaluation for members
INSERT INTO evaluations (project_id, user_id, professor_id, feedback, score)
SELECT 
    project_members.project_id,
    project_members.user_id,         -- student
    users.id,               -- professor (from users table)
    feedback,
    score
FROM project_members
JOIN users ON users.id = evaluations.professor_id
JOIN users p ON p.id = professor_id
WHERE pm.project_id = project_id
  AND pm.user_id = student_id
  AND pm.role = 'member'
  AND p.role = 'professor';

--average score for project
SELECT 
    project_id,
    project_title,
    AVG(score) AS average_score
FROM evaluations
GROUP BY project_id;

--project evaluation details
SELECT 
    project_id, title, project.description, feedback, score, user.name AS student_name, users.name AS professor_name 
FROM evaluations
JOIN projects ON projects.project_id = evaluations.project_id
JOIN users ON users.id = evaluations.user_id
JOIN users ON users.id = evaluations.professor_id
WHERE project_id = 001;

/*SELECT 
    u_student.name AS student_name,
    u_prof.name AS professor_name,
    e.score,
    e.feedback
FROM evaluations e
JOIN users u_student 
    ON u_student.id = e.user_id 
    AND u_student.role = 'student'
JOIN users u_prof 
    ON u_prof.id = e.professor_id 
    AND u_prof.role = 'professor'
WHERE e.project_id = :project_id;*/
