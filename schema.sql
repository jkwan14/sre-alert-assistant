
CREATE TABLE alerts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert TEXT NOT NULL,
    explanation TEXT NOT NULL,
    severity TEXT NOT NULL,
    possible_causes TEXT NOT NULL,
    next_steps TEXT NOT NULL,
    source TEXT NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
