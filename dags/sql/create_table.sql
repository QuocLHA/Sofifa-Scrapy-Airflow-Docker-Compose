CREATE TABLE IF NOT EXISTS clean_data (
    sofifa_id INT PRIMARY KEY,
    long_name varchar(50),
    short_name varchar(50),
    photo_url varchar(50),
    positions varchar(20),
    age int,
    dob date,
    height_cm int,
    weight_kg int,
    overall_rating int,
    potential_rating int,
    value_euro int,
    wage_euro int,
    preferred_foot varchar(10),
    weak_foot int,
    skill_moves int,
    international_reputation int,
    work_rate varchar(50),
    body_type varchar(50),
    real_face varchar(10),
    release_clause_euro int,
    club varchar(50),
    club_overall int,
    national varchar(50),
    attack_crossing int,
    attack_finishing int,
    attack_heading_accuracy int,
    attack_short_passing int,
    attack_volley int,
    skill_dribbling int,
    skill_curve int,
    skill_fk_accuracy int,
    skill_long_passing int,
    skill_ball_control int,
    movement_acceleration int,
    movement_sprint_speed int,
    movement_agility int,
    movement_reaction int,
    movement_balance int,
    power_shot int,
    power_jumping int,
    power_stamina int,
    power_strength int,
    power_long_shot int,
    mentality_aggression int,
    mentality_interception int,
    mentality_positioning int,
    mentality_vision int,
    mentality_penalty int,
    mentality_composure int,
    defensive_awareness int,
    defensive_standing_tackle int,
    defensive_sliding_tackle int,
    goalkeeping_diving int,
    goalkeeping_handling int,
    goalkeeping_composure int,
    goalkeeping_kicking int,
    goalkeeping_positioning int,
    player_traits varchar(150),
    player_hashtags varchar(100)
);

CREATE TABLE IF NOT EXISTS dim_club (
    club_id serial PRIMARY KEY,
    club varchar(50),
    club_overall int
);

CREATE TABLE IF NOT EXISTS dim_national (
    national_id serial PRIMARY KEY,
    national varchar(50)
);

CREATE TABLE IF NOT EXISTS dim_work_rate (
    workrate_id serial PRIMARY KEY,
    work_rate varchar(50)
);

CREATE TABLE IF NOT EXISTS dim_real_face (
    realface_id serial PRIMARY KEY,
    real_face varchar(10)
);

CREATE TABLE IF NOT EXISTS dim_stat (
    stat_id serial PRIMARY KEY,
    overall_rating int,
    potential_rating int,
    preferred_foot varchar(10),
    weak_foot int,
    skill_moves int,
    international_reputation int,
    attack_crossing int,
    attack_finishing int,
    attack_heading_accuracy int,
    attack_short_passing int,
    attack_volley int,
    skill_dribbling int,
    skill_curve int,
    skill_fk_accuracy int,
    skill_long_passing int,
    skill_ball_control int,
    movement_acceleration int,
    movement_sprint_speed int,
    movement_agility int,
    movement_reaction int,
    movement_balance int,
    power_shot int,
    power_jumping int,
    power_stamina int,
    power_strength int,
    power_long_shot int,
    mentality_aggression int,
    mentality_interception int,
    mentality_positioning int,
    mentality_vision int,
    mentality_penalty int,
    mentality_composure int,
    defensive_awareness int,
    defensive_standing_tackle int,
    defensive_sliding_tackle int,
    goalkeeping_diving int,
    goalkeeping_handling int,
    goalkeeping_composure int,
    goalkeeping_kicking int,
    goalkeeping_positioning int
);

CREATE TABLE IF NOT EXISTS dim_transfer (
    transfer_id serial PRIMARY KEY,
    value_euro int,
    wage_euro int,
    release_clause_euro int
);

CREATE TABLE IF NOT EXISTS dim_appearence (
    appearence_id serial PRIMARY KEY,
    height_cm int,
    weight_kg int
);

CREATE TABLE IF NOT EXISTS dim_body_type (
    bodytype_id serial PRIMARY KEY,
    body_type varchar(50)
);

CREATE TABLE IF NOT EXISTS dim_position (
    position_id serial PRIMARY KEY,
    positions varchar(20)
);

CREATE TABLE IF NOT EXISTS dim_basic_infor (
    basicinfor_id serial PRIMARY KEY,
    long_name varchar(50),
    short_name varchar(50),
    photo_url varchar(50),
    age int,
    dob date
);

CREATE TABLE IF NOT EXISTS dim_trait (
    trait_id serial PRIMARY KEY,
    player_traits varchar(150)
);

CREATE TABLE IF NOT EXISTS dim_hashtag (
    hashtag_id serial PRIMARY KEY,
    player_hashtags varchar(100)
);

CREATE TABLE IF NOT EXISTS fact_player (
    sofifa_id int PRIMARY KEY,
    club_id int,
    national_id int,
    workrate_id int,
    realface_id int,
    stat_id int,
    transfer_id int,
    appearence_id int,
    bodytype_id int,
    position_id int,
    basicinfor_id int,
    trait_id int,
    hashtag_id int
);