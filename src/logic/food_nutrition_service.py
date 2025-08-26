import db.database as DB


def get_food_nutrition_info(food_names: list):
    """
    주어진 음식 이름 목록을 기반으로 음식 영양 정보를 조회합니다.

    '외식'으로 분류된 음식을 우선적으로 반환하며, 없을 경우 첫 번째 검색 결과를 반환합니다.
    리스트에 여러 음식이 있어도 첫 번째 음식에 대한 결과만 처리하고 반환합니다.

    Args:
        food_names (list): 조회할 음식 이름의 리스트.

    Returns:
        dict: 조회된 음식의 영양 정보 데이터 (딕셔너리).
              데이터를 찾지 못한 경우 None을 반환합니다.
    """
    for food_name in food_names:
        food_datas = DB.get_food_info_by_name(food_name)

        if len(food_datas) < 1:
            return None
        else:
            for food_data in food_datas:
                if '외식 ' in food_data["food_origin_name"]:
                    return food_data

            return food_datas[0]
    return None


if __name__ == "__main__":
    print(get_food_nutrition_info(['육회']))
