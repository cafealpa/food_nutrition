import src.db.database as DB
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.agents import create_openai_functions_agent, tool, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

system_prompt = """
    역할: 당신은 식품 영양 분석 전문가입니다.
    목표:
    1) 제공된 도구(get_food_info)로 입력된 음식의 영양 데이터를 조회합니다.
    2) 조회된 데이터가 없으면,  일반적인 영양 지식을 기반으로 해당 음식의 성분을 추정합니다.
    3) 영양 데이터를 근거로 건강 점수(0~100)를 산출하고, 과/부족 항목을 설명합니다.
    4) 개선 팁(예: 나트륨 낮추기, 단백질 보완)을 제안합니다.
    규칙:
    - 데이터가 있으면 반드시 도구를 우선 사용할 것.
    - 데이터가 없으면 추정하되, 반드시 실제 음식 유형에 맞도록 할 것.
    - 출력은 마지막에 깔끔한 한국어 문단으로 제공.,
"""

human_prompt = """
    {input}
    출력 형식 가이드:
    1) 건강 점수: NN/100
    2) 이유: (성분별 근거)
    3) 개선 팁: (실천 가능한 제안 2~4개)"),
"""


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


@tool
def get_food_info(food_name: str) -> str:
    """주어진 음식 이름에 해당하는 영양 정보를 반환합니다."""
    result = get_food_nutrition_info([food_name])
    if result:
        return str(result)
    else:
        return None


def ask_llm(food_name):
    nutrition_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools=[get_food_info], prompt=nutrition_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[get_food_info], verbose=True)

    input_prompt = f"""
        {food_name}의 영양 정보를 바탕으로 
        1) 건강 점수를 0~100으로 매겨줘.
        2) 점수 이유를 성분별로 설명해줘.
        3) 개선 팁을 알려줘.
    """
    response = agent_executor.invoke({"input": input_prompt})
    return response["output"]

if __name__ == "__main__":
    print(ask_llm("김치찜"))
