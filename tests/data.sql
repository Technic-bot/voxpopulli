PRAGMA foreign_keys = ON;

INSERT INTO polls (poll_id, name, created_at, closes_at)
    VALUES 
        (123, "Sunday poll", date('now'), date('now', '+7 days') ),
        (456, "90s poll", "1996-07-01", date('now', '+7 days') ),
        (789, "MkII poll", date('now', '-1 days'), date('now', "+7 days") );

INSERT INTO suggestions (suggestion_id, poll_id, text)
    VALUES
        (1, 123, "Mario Jumping over a koopa"),
        (2, 456, "Kamen rider black transforming"),
        (3, 456, "Zelda on a picnic"),
        (4, 456, "Cross country roadtrip"),
        (5, 456, "Girls in a museum exhibit"),
        (6, 456, "CSI cosplay"),
        (7, 123, "Willow's Origin Prequel: Maya and Willow's encounter"),
        (17, 789, "Kat sits in the park feeding pidgeons"),
        (18, 789, "Short haired Raine in wolf form"),
        (19, 789, "Flora in lynx form"),
        (20, 789, "Zen and Natani assasin training"),
        (21, 789, "Bug modern trio"),
        (22, 789, "Main Trio playing football");

INSERT INTO ballots (ballot_id, poll_id, submited_at, voter_id) 
    VALUES 
        (21, 456, date('now'), "Jason"),
        (22, 789, '2026-06-21T05:03:03.867991+00:00','Florb'),
        (26, 789, '2026-06-20T05:03:02.847981+00:00','Tec'),
        (27, 789, date('now'), 'Noxtella'),
        (28, 789, date('now', '-1 minute'), 'HeavenlyMotors'),
        (29, 789, date('now', '-2 minute'), 'Iron');


INSERT INTO rankings (suggestion_id, ballot_id, ranked) 
    VALUES 
        (3,  21, 2),
        (2,  21, 1),
        (19, 22, 0),
        (18, 26, 0),
        (19, 26, 1),
        (17, 26, 2),
        (20, 27, 0),
        (18, 27, 1),
        (17, 27, 2),
        (19, 27, 3),
        (20, 28, 0),
        (22, 28, 1),
        (19, 29, 0),
        (17, 29, 2),
        (21, 29, 3);
