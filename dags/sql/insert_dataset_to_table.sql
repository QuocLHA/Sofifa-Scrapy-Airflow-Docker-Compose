insert into dim_club (club,club_overall)
select club,club_overall
from clean_data
group by club, club_overall
order by club_overall;

insert into dim_national(national)
select national
from clean_data
group by national;

insert into dim_work_rate(work_rate)
select work_rate
from clean_data
group by work_rate;

insert into dim_real_face(real_face)
select real_face
from clean_data
group by real_face;

insert into dim_stat(overall_rating, potential_rating, preferred_foot, weak_foot, skill_moves, international_reputation, attack_crossing, attack_finishing, attack_heading_accuracy, attack_short_passing, attack_volley, skill_dribbling, skill_curve, skill_fk_accuracy, skill_long_passing, skill_ball_control, movement_acceleration, movement_sprint_speed, movement_agility, movement_reaction, movement_balance, power_shot, power_jumping, power_stamina, power_strength, power_long_shot, mentality_aggression, mentality_interception, mentality_positioning, mentality_vision, mentality_penalty, mentality_composure, defensive_awareness, defensive_standing_tackle, defensive_sliding_tackle, goalkeeping_diving, goalkeeping_handling, goalkeeping_composure, goalkeeping_kicking, goalkeeping_positioning)
select overall_rating, potential_rating, preferred_foot, weak_foot, skill_moves, international_reputation, attack_crossing, attack_finishing, attack_heading_accuracy, attack_short_passing, attack_volley, skill_dribbling, skill_curve, skill_fk_accuracy, skill_long_passing, skill_ball_control, movement_acceleration, movement_sprint_speed, movement_agility, movement_reaction, movement_balance, power_shot, power_jumping, power_stamina, power_strength, power_long_shot, mentality_aggression, mentality_interception, mentality_positioning, mentality_vision, mentality_penalty, mentality_composure, defensive_awareness, defensive_standing_tackle, defensive_sliding_tackle, goalkeeping_diving, goalkeeping_handling, goalkeeping_composure, goalkeeping_kicking, goalkeeping_positioning
from clean_data;

insert into dim_transfer(value_euro, wage_euro, release_clause_euro)
select value_euro, wage_euro, release_clause_euro
from clean_data
group by value_euro, wage_euro, release_clause_euro;

insert into dim_appearence(height_cm, weight_kg)
select height_cm, weight_kg
from clean_data
group by  weight_kg, height_cm;

insert into dim_body_type(body_type)
select body_type
from clean_data
group by  body_type;

insert into dim_position(positions)
select positions
from clean_data
group by positions;

insert into dim_basic_infor(long_name, short_name, photo_url, age, dob)
select long_name, short_name, photo_url, age, dob
from clean_data;

insert into dim_trait(player_traits)
select player_traits
from clean_data
group by player_traits;

insert into dim_hashtag(player_hashtags)
select player_hashtags
from clean_data
group by player_hashtags;

insert into fact_player(sofifa_id, club_id, national_id, workrate_id, realface_id, stat_id, transfer_id, appearence_id, bodytype_id, position_id, basicinfor_id, trait_id, hashtag_id)
select sofifa_id, club_id, national_id, workrate_id, realface_id, stat_id, transfer_id, appearence_id, bodytype_id, position_id, basicinfor_id, trait_id, hashtag_id
from clean_data as cd
left join dim_club
    on dim_club.club = cd.club and dim_club.club_overall = cd.club_overall
left join dim_national
    on dim_national.national = cd.national
left join dim_work_rate
    on dim_work_rate.work_rate = cd.work_rate
left join dim_real_face
    on dim_real_face.real_face = cd.real_face
left join dim_stat as ds
    on ds.overall_rating=cd.overall_rating and ds.potential_rating=cd.potential_rating and ds.preferred_foot=cd.preferred_foot and ds.weak_foot=cd.weak_foot
    and ds.skill_moves=cd.skill_moves and ds.international_reputation=cd.international_reputation and ds.attack_crossing=cd.attack_crossing
    and ds.attack_finishing=cd.attack_finishing and ds.attack_heading_accuracy=cd.attack_heading_accuracy and ds.attack_short_passing=cd.attack_short_passing
    and ds.attack_volley=cd.attack_volley and ds.skill_dribbling=cd.skill_dribbling and ds.skill_curve=cd.skill_curve and ds.skill_fk_accuracy=cd.skill_fk_accuracy
    and ds.skill_long_passing=cd.skill_long_passing and ds.skill_ball_control=cd.skill_ball_control and ds.movement_acceleration=cd.movement_acceleration
    and ds.movement_sprint_speed=cd.movement_sprint_speed and ds.movement_agility=cd.movement_agility and ds.movement_reaction=cd.movement_reaction
    and ds.movement_balance=cd.movement_balance and ds.power_shot=cd.power_shot and ds.power_jumping=cd.power_jumping and ds.power_stamina=cd.power_stamina
    and ds.power_strength=cd.power_strength and ds.power_long_shot=cd.power_long_shot and ds.mentality_aggression=cd.mentality_aggression
    and ds.mentality_interception=cd.mentality_interception and ds.mentality_positioning=cd.mentality_positioning and ds.mentality_vision=cd.mentality_vision
    and ds.mentality_penalty=cd.mentality_penalty and ds.mentality_composure=cd.mentality_composure and ds.defensive_awareness=cd.defensive_awareness
    and ds.defensive_standing_tackle=cd.defensive_standing_tackle and ds.defensive_sliding_tackle=cd.defensive_sliding_tackle
    and ds.goalkeeping_diving=cd.goalkeeping_diving and ds.goalkeeping_handling=cd.goalkeeping_handling and ds.goalkeeping_composure=cd.goalkeeping_composure
    and ds.goalkeeping_kicking=cd.goalkeeping_kicking and ds.goalkeeping_positioning=cd.goalkeeping_positioning
left join dim_transfer
    on dim_transfer.value_euro=cd.value_euro and dim_transfer.wage_euro=cd.wage_euro and dim_transfer.release_clause_euro=cd.release_clause_euro
left join dim_appearence
    on dim_appearence.height_cm=cd.height_cm and dim_appearence.weight_kg=cd.weight_kg
left join dim_body_type
    on dim_body_type.body_type=cd.body_type
left join dim_position
    on dim_position.positions=cd.positions
left join dim_basic_infor
    on dim_basic_infor.long_name=cd.long_name and dim_basic_infor.short_name=cd.short_name and dim_basic_infor.photo_url=cd.photo_url
    and dim_basic_infor.age=cd.age and dim_basic_infor.dob=cd.dob
left join dim_trait
    on dim_trait.player_traits=cd.player_traits
left join dim_hashtag
    on dim_hashtag.player_hashtags=cd.player_hashtags;
