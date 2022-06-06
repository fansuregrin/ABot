import json
import random


dish_data_path = 'plugins/eatwhat/dish_data.json'

def gen_random_dish():
    with open(dish_data_path, 'r') as fp:
        dish_info = json.load(fp)
    rand_type = list(dish_info.keys())[random.randint(0, len(dish_info)-1)]
    rand_dish = dish_info[rand_type][random.randint(0, len(dish_info[rand_type])-1)]
    outcome = '推荐您吃{}\n[CQ:image,file={}]'.format(rand_dish['dish_title'], rand_dish['dish_pic_url'])
    
    return outcome


if __name__ == '__main__':
    print(gen_random_dish())