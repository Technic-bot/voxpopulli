INSERT INTO polls (poll_id, name, created_at, closes_at)
    VALUES 
        (123, "Sunday poll", date('now'), date('now', '+7 days')),
        (456, "90s poll", "1996-07-01", "2020-07-02") ;

INSERT INTO suggestions (suggestion_id, poll_id, text)
    VALUES
        (1, 123, "Mario Jumping over a koopa"),
        (2, 456, "Kamen rider black transforming"),
        (3, 456, "Zelda on a picnic");
