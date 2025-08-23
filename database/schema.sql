DROP TABLE IF EXISTS prevention_question CASCADE;
DROP TABLE IF EXISTS prevention_case CASCADE;

CREATE TABLE prevention_case (
    id SERIAL PRIMARY KEY,
    creation_time TIMESTAMP,
    title TEXT,
    damage_desc TEXT,
    facade TEXT,
    basement TEXT,
    roof TEXT,
    heating TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    preventions TEXT
);

CREATE TABLE prevention_question (
    id SERIAL PRIMARY KEY,
    prevention_case_id INTEGER,
    question_text TEXT,
    answer_text TEXT,

    CONSTRAINT fk_prevention_case FOREIGN KEY (prevention_case_id)
        REFERENCES prevention_case (id)
        ON DELETE CASCADE
);
