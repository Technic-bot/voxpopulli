CREATE TABLE poll (
    poll_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    closes_at   TEXT NOT NULL
);

CREATE TABLE suggestion (
    suggestion_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id         INTEGER NOT NULL,
    text            TEXT NOT NULL,
    FOREIGN KEY(poll_id) REFERENCES poll(poll_id)
);

CREATE TABLE ballot (
    ballot_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id     INTEGER NOT NULL,
    submited_at TEXT NOT NULL,
    voter_id TEXT,
        UNIQUE(poll_id, voter_id),
    FOREIGN KEY(poll_id) REFERENCES poll(poll_id)
);

CREATE TABLE ranking (
    suggestion_id   INTEGER NOT NULL,
    ballot_id       INTEGER NOT NULL,
    ranked          INTEGER NOT NULL,
    PRIMARY KEY (ballot_id, suggestion_id),
    FOREIGN KEY(suggestion_id) REFERENCES poll(suggestion_id),
    FOREIGN KEY(ballot_id) REFERENCES poll(ballot_id)
);

