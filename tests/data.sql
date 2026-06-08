PRAGMA foreign_keys = ON;

INSERT INTO polls (poll_id, name, created_at, closes_at)
    VALUES 
        (123, "Sunday poll", date('now'), date('now', '+7 days')),
        (456, "90s poll", "1996-07-01", date('now', '+7 days') );

INSERT INTO suggestions (suggestion_id, poll_id, text)
    VALUES
        (1, 123, "Mario Jumping over a koopa"),
        (2, 456, "Kamen rider black transforming"),
        (3, 456, "Zelda on a picnic"),
        (4, 456, "Cross country roadtrip"),
        (5, 456, "Girls in a museum exhibit"),
        (6, 456, "CSI cosplay"),
        (7, 123, "Willow's Origin Prequel: Maya and Willow's encounter");

INSERT INTO ballots (ballot_id, poll_id, submited_at, voter_id) 
    VALUES 
        (21, 456, date('now'), "Jason");

INSERT INTO rankings (suggestion_id, ballot_id, ranked) 
    VALUES 
        (3, 21, 2),
        (2, 21, 1);
