INSERT INTO polls (poll_id, name, created_at, closes_at)
    VALUES 
        (123, "Mario Jumping over a koopa", date('now'), date('now', '+7 days')),
        (456, "Geats transforming", "1996-07-01", "2020-07-02") ;
