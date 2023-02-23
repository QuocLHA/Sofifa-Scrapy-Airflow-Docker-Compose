# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import numpy as np
from numpy import *

class ASofifaSpider(scrapy.Spider):
    name='players_stats'

    def __init__(self):
        try:
            with open('./data/json/players_urls.json') as json_data:
                self.players = json.load(json_data)
            self.player_count = 1
        except IOError:
            logging.error('Error: File does not appear to exist. \n Try running `scrapy crawl players_urls` if not run before.')

    def start_requests(self):
        urls = [
            'https://sofifa.com/player/231747?units=mks' # ---> Top1 overall rating  example page
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for player in response.css('.info'):
            player_id = player.xpath('//div[@class="card" and h5="Profile"]//li[label = "ID"]/text()').get()
            player_short_name = player.xpath('//body[@class="is-preload "]//div[@class="header"]//h1/text()').get()
            player_name_info = player.xpath('//div[@class="info"]/h1/text()').get()
            player_name = player_name_info.split('(')[0].strip()
            player_info = player.xpath('//div[@class="meta ellipsis"]/text()[last()]').get()
            player_info = player_info.split()

            for info in player_info:
                if "\'" in info:
                    player_info.remove(info)
                elif "lbs" in info:
                    player_info.remove(info)
                else:
                    None
            for info in player_info:
                if "/" in info:
                    player_info.remove(info)

            #player_info = [info for info in player_info if info != ' ']
            player_position = player.xpath('//div[@class="meta ellipsis"]//span/text()').getall()
            player_url_photo = player.xpath('//div[@class="bp3-card player" ]//img/@data-src').getall()[0]

            # Add stats_names and values (Crossing, finishing) + goalkeeper stats_names and values (GK Diving, GK Reflexes)
            player_stats = player.xpath('//div[@class="card"]//ul//li/span[2]//text()').re(r'[a-zA-Z ]+')
            player_stats.insert(-3, "Composure")
            player_stats = player_stats + player.xpath('//div[@class="card" and h5="Goalkeeping"]//ul//li/text()').getall()
            player_stats_values = player.xpath('//div[@class="card" and h5 !="Profile" and h5 != "Traits" and not(img)]/ul//li/span[1]//text()').getall()
            # Compensating for the missing "Composure" field
            _player_composure_value = player.xpath('//div[@class="card"]//ul//li[text()=" Composure"]/text()').get()
            if _player_composure_value != None:
                player_stats_values.insert(25, 50)           

            # Overall rating, potential rating + value, wage names and values
            primary_stats = player.xpath('//div[@class="sub"]//text()').getall()
            primary_stats_values = player.xpath('//section[@class="card spacing"]/div[@class = "block-quarter"]/div/span[1]/text()').getall()
            primary_stats_values = primary_stats_values + [stat for stat in player.xpath('//section[@class="card spacing"]/div[@class = "block-quarter"]/div/text()').getall() if stat != ' ']
            
            # Add the club and nationality names and the respective team rating
            player_teams = player.xpath('//div[@class="card"]//h5//a/text()').getall()
            player_teams_values = player.xpath('//div[@class="card"]//ul[@class="ellipsis pl"]//li[1]//span//text()').re(r'\w+')

            # Add profile stats (Prefeered foot, Weak Foot, International Reputation) and its values
            player_profile_stats = player.xpath('//div[@class="card" and h5="Profile"]//label/text()').getall()
            player_profile_values = player.xpath('//div[@class="card" and h5="Profile"]//li[label != "ID"]/text()').getall()
            player_profile_values = [val for val in player_profile_values if val != ' ']
            player_profile_values = player_profile_values + (player.xpath('//div[@class="card" and h5="Profile"]//li/span[not (@class)]/text()').getall())

            # Add player most played position
            player_primary_position = player.xpath('//div[@class="center"]//div[@class="col col-4"]//li[@class="ellipsis"]//span[@class="pos pos21"]/text()').get()

            # Add player specialities (#Acrobat, #Dribbler) and Traits (Finesse shot, Playmaker)
            player_tags = player.xpath('//div[@class="card" and h5="Player Specialities"]//ul//li//a/text()').getall()
            player_traits = player.xpath('//div[@class="card" and h5="Traits"]//ul//li//text()').getall()

            # Add player club photo url and country photo url
            player_country = player.xpath('//div[@class="meta ellipsis"]/a/@title').get()
            player_country_logo_url = player.xpath('//div[@class="meta ellipsis"]//img/@data-src').get()
            player_clubs_list = player.xpath('//div[@class="block-quarter"][3]//div[@class="card"]//h5/a/text()').getall()
            player_clubs_logo_list = player.xpath('//div[@class="block-quarter"][3]//div[@class="card"]/*[not(self::h5)]/@data-src').getall()
            
            #player_logo_urls = {}
            #country = {'name': player_country, 'url': player_country_logo_url}
            #player_logo_urls.update({'country': country})
            #for k, v in zip(player_clubs_list, player_clubs_logo_list):
            #    if k == player_country:
            #        nationalClub = {'name': k, 'url': v}
            #        player_logo_urls.update({'nationalClub': nationalClub})
            #    else:
            #        club = {'name': k, 'url': v}
            #        player_logo_urls.update({'club': club})



            ###########################################################

            # Age 30 (Jun 24, 1987) 170cm 72kg'
            age, month, day, year, height, weight = player_info
            age = age[:-4]
            month = month.replace('(', '')
            day = int(day.replace(',', ''))
            year = int(year.replace(')', ''))
            height = int(height[:-2])
            weight = int(weight[:-2])

            stats = {k:v for k, v in zip(primary_stats, primary_stats_values)}
            stats["Overall Rating"] = int(stats["Overall Rating"])
            stats["Potential"] = int(stats["Potential"])
            
            extra = {k:v for k, v in zip(player_profile_stats, player_profile_values)}
            extra["International Reputation"] = int(extra["International Reputation"])
            extra["Weak Foot"] = int(extra["Weak Foot"])
            extra["Skill Moves"] = int(extra["Skill Moves"])

            # teams
            teams_lst = []
            teams_overall_lst = []
            for i in player_teams:
                teams_lst.append(i.replace(' ','',1))
            for j in player_teams_values:
                teams_overall_lst.append(int(j))

            if len(teams_lst) < 2 and len(teams_overall_lst) < 2:
                teams_lst.append('None')
                teams_overall_lst.append(0)

            """ Vì đôi khi vị trí clb không phải lúc nào cũng phải nằm đâu tiên, nên check các element của lst player_country
            với cột national, nếu element nào giống thì không lấy, element còn lại sẽ là club.
            """     
            if str(teams_lst[0]) == str(player_country):
                club = {'club':teams_lst[1]}
                club_overall = {'club_overall':teams_overall_lst[1]}
            else:
                club = {'club':teams_lst[0]}
                club_overall = {'club_overall':teams_overall_lst[0]}

            #national = {'national':teams_lst[1].replace(' ','',1)}
            national = {'national':str(player_country)}
            
            # không xuất điểm tổng quan của đội tuyển quốc gia vì ít đội có điểm tổng quan.
            #national_overall = {'national_overall':int(teams_overall_lst[1])}

            # attacking
            attacking = {'attacking':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[:5], player_stats_values[:5])}}
            attacking_value_lst = []
            for i in player_stats_values[:5]:
                attacking_value_lst.append(int(i))
            attack_crossing = {'attack_crossing':attacking_value_lst[0]}
            attack_finishing = {'attack_finishing':attacking_value_lst[1]}
            attack_heading_accuracy = {'attack_heading_accuracy':attacking_value_lst[2]}
            attack_short_passing = {'attack_short_passing':attacking_value_lst[3]}
            attack_volley = {'attack_volley':attacking_value_lst[4]}

            # skill
            skill = {'skill':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[5:10], player_stats_values[5:10])}}
            skill_value_lst = []
            for i in player_stats_values[5:10]:
                skill_value_lst.append(int(i))
            skill_dribbling = {'skill_dribbling':skill_value_lst[0]}
            skill_curve = {'skill_curve':skill_value_lst[1]}
            skill_fk_accuracy = {'skill_fk_accuracy':skill_value_lst[2]}
            skill_long_passing = {'skill_long_passing':skill_value_lst[3]}
            skill_ball_control = {'skill_ball_control':skill_value_lst[4]}

            # movement
            movement = {'movement':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[10:15], player_stats_values[10:15])}}
            movement_value_lst = []
            for i in player_stats_values[10:15]:
                movement_value_lst.append(int(i))
            movement_acceleration = {'movement_acceleration':movement_value_lst[0]}
            movement_sprint_speed = {'movement_sprint_speed':movement_value_lst[1]}
            movement_agility = {'movement_agility':movement_value_lst[2]}
            movement_reaction = {'movement_reaction':movement_value_lst[3]}
            movement_balance = {'movement_balance':movement_value_lst[4]}

            # power
            power = {'power':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[15:20], player_stats_values[15:20])}}
            power_value_lst = []
            for i in player_stats_values[15:20]:
                power_value_lst.append(int(i))
            power_shot = {'power_shot':power_value_lst[0]}
            power_jumping = {'power_jumping':power_value_lst[1]}
            power_stamina = {'power_stamina':power_value_lst[2]}
            power_strength = {'power_strength':power_value_lst[3]}
            power_long_shot = {'power_long_shot':power_value_lst[4]}

            # mentality
            mentality = {'mentality':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[20:26], player_stats_values[20:26])}}
            mentality_value_lst = []
            for i in player_stats_values[20:26]:
                mentality_value_lst.append(int(i))
            mentality_aggression = {'mentality_aggression':mentality_value_lst[0]}
            mentality_interception = {'mentality_interception':mentality_value_lst[1]}
            mentality_positioning = {'mentality_positioning':mentality_value_lst[2]}
            mentality_vision = {'mentality_vision':mentality_value_lst[3]}
            mentality_penalty = {'mentality_penalty':mentality_value_lst[4]}
            mentality_composure = {'mentality_composure':mentality_value_lst[5]}

            # defending
            defending = {'defending':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[26:29], player_stats_values[26:29])}}
            defending_value_lst = []
            for i in player_stats_values[26:29]:
                defending_value_lst.append(int(i))
            defensive_awareness = {'defensive_awareness':defending_value_lst[0]}
            defensive_standing_tackle = {'defensive_standing_tackle':defending_value_lst[1]}
            defensive_sliding_tackle = {'defensive_sliding_tackle':defending_value_lst[2]}

            # goalkeeping
            goalkeeping = {'goalkeeping':{k.replace(' ', ''):int(v) for k, v in zip(player_stats[29:], player_stats_values[29:])}}
            goalkeeping_value_lst = []
            for i in player_stats_values[29:]:
                goalkeeping_value_lst.append(int(i))
            goalkeeping_diving = {'goalkeeping_diving':goalkeeping_value_lst[0]}
            goalkeeping_handling = {'goalkeeping_handling':goalkeeping_value_lst[1]}
            goalkeeping_composure = {'goalkeeping_composure':goalkeeping_value_lst[2]}
            goalkeeping_kicking = {'goalkeeping_kicking':goalkeeping_value_lst[3]}
            goalkeeping_positioning = {'goalkeeping_positioning':goalkeeping_value_lst[4]}


            player_info_dict = {
                    'id': player_id,
                    'name': player_name,
                    'short_name': player_short_name,
                    'photo_url': player_url_photo,
                    'positions': [position for position in player_position if position.isupper()],
                    'age': age,
                    'birth_date': '{}/{}/{}'.format(year, month, day),
                    'height': height,
                    'weight': weight,
            }
            player_info_dict.update(stats)
            player_info_dict.update(extra)
            player_info_dict.update(club)
            player_info_dict.update(club_overall)
            player_info_dict.update(national)
            #player_info_dict.update(national_overall)

            player_info_dict.update(attack_crossing)     
            player_info_dict.update(attack_finishing)     
            player_info_dict.update(attack_heading_accuracy)     
            player_info_dict.update(attack_short_passing)     
            player_info_dict.update(attack_volley)     

            player_info_dict.update(skill_dribbling)     
            player_info_dict.update(skill_curve)     
            player_info_dict.update(skill_fk_accuracy)     
            player_info_dict.update(skill_long_passing)     
            player_info_dict.update(skill_ball_control)  

            player_info_dict.update(movement_acceleration)     
            player_info_dict.update(movement_sprint_speed)     
            player_info_dict.update(movement_agility)     
            player_info_dict.update(movement_reaction)     
            player_info_dict.update(movement_balance)  

            player_info_dict.update(power_shot)     
            player_info_dict.update(power_jumping)     
            player_info_dict.update(power_stamina)     
            player_info_dict.update(power_strength)     
            player_info_dict.update(power_long_shot)  

            player_info_dict.update(mentality_aggression)     
            player_info_dict.update(mentality_interception)     
            player_info_dict.update(mentality_positioning)     
            player_info_dict.update(mentality_vision)     
            player_info_dict.update(mentality_penalty)  
            player_info_dict.update(mentality_composure)  

            player_info_dict.update(defensive_awareness)     
            player_info_dict.update(defensive_standing_tackle)     
            player_info_dict.update(defensive_sliding_tackle)     

            player_info_dict.update(goalkeeping_diving)     
            player_info_dict.update(goalkeeping_handling)     
            player_info_dict.update(goalkeeping_composure)     
            player_info_dict.update(goalkeeping_kicking)     
            player_info_dict.update(goalkeeping_positioning)  

            #player_info_dict.update(attacking)
            #player_info_dict.update(skill)
            #player_info_dict.update(movement)
            #player_info_dict.update(power)
            #player_info_dict.update(mentality)
            #player_info_dict.update(defending)
            #player_info_dict.update(goalkeeping)

            if len(player_traits) == 0:
                player_traits.append('None')
            player_skills_dict = {'player_traits': player_traits}
            player_info_dict.update(player_skills_dict)

            if len(player_tags) == 0:
                player_tags.append('None')
            player_hashtags = {'player_hashtags': player_tags}
            player_info_dict.update(player_hashtags)


            #player_logos_dict = {'logos': player_logos_urls}
            #player_info_dict.update(player_logos_dict)

            logging.info('*******************  ' + str(self.player_count) + '  *******************' + '\n\n\n')
            yield player_info_dict

            if self.player_count < len(self.players):
                next_page_url = 'https://sofifa.com' + self.players[self.player_count]['player_url'] + '?units=mks'
                self.player_count += 1
                yield scrapy.Request(url=next_page_url, callback=self.parse)
