import sqlite3

DB_PATH = '/Users/james/Documents/Projects/products/ai_groom_lecture/projects/food_nutrition/food_nutrition.db'

def get_food_nutrition_data(limit=10):
    """
    food_nutrition 테이블에서 데이터를 조회합니다.
    :param limit: 조회할 데이터의 최대 개수
    :return: 음식 영양 데이터 리스트
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 컬럼명으로 접근 가능하도록 설정
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM food_nutrition LIMIT {limit}")
        rows = cursor.fetchall()

        # sqlite3.Row 객체를 dict 리스트로 변환
        data = [dict(row) for row in rows]
        return data

    except sqlite3.Error as e:
        print(f"데이터베이스 오류: {e}")
        return []
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    food_data = get_food_nutrition_data(5)
    if food_data:
        for item in food_data:
            print(item)