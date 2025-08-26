import db.database as DB

def get_food_nutrition_info(food_names: list):
    for food_name in food_names:
        food_datas = DB.get_food_info_by_name(food_name)

        if len(food_datas) < 1:
            return None
        else:
            for food_data in food_datas:
                 if '외식 'in food_data["food_origin_name"]:
                     return food_data

            return food_datas[0]
    return None


if __name__ == "__main__":
    print(get_food_nutrition_info(['육회']))











