from datetime import datetime
from pydantic import BaseModel, Field
import asyncio, json

from langchain_community.tools.tavily_search import TavilySearchResults
from app.config.settings import settings

from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

llm = ChatOpenAI(model_name="gpt-4",temperature=0.6,openai_api_key=settings.OPENAI_API_KEY)
search = TavilySearchResults(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)

class TravelState(BaseModel):
    destination: str
    start_date: str
    end_date: str
    raw_info: str | None = None
    summary: str | None = None
    schedule: str | None = None

class TravelSearchOutput(BaseModel):
    attraction: str = Field(description="旅遊景點")
    food: str = Field(description="旅遊美食")
    activity: str = Field(description="旅遊活動")
    transportation: str = Field(description="交通方式")
    accommodation: str = Field(description="住宿")


def search_node(state: TravelState):
    destination = state.destination
    start_date = state.start_date
    end_date = state.end_date

    queries = {
        "景點": f"{destination} {start_date} 至 {end_date} 景點推薦 行程安排",
        # "美食": f"{destination} {start_date} 至 {end_date} 在地美食 餐廳 推薦",
        # "活動": f"{destination} {start_date} 至 {end_date} 節慶 活動 展覽 表演",
        # "交通": f"{destination} {start_date} 至 {end_date} 交通方式 地鐵 公車 火車 路線 指南",
        # "住宿": f"{destination} {start_date} 至 {end_date} 住宿推薦"
    }

    results = []
    for topic, query in queries.items():
        res = search.run(query)
        results.append(f"【{topic}】\n{res[:200]}")

    state.raw_info = "\n\n".join(results)
    return state
    
def summary_node(state: TravelState):
    parser = JsonOutputParser(pydantic_object=TravelSearchOutput)
    format_instructions = parser.get_format_instructions()

    template = PromptTemplate(
        input_variables=["content"],
        template=(
            """你是一位專業旅遊規劃助理，請閱讀以下旅遊資訊內容：{content}
            請將資訊整理成包含 景點、美食、活動、交通、住宿五個欄位的 JSON，用繁體中文表達。"""
            # 請將資訊整理成包含 景點、美食兩個欄位的 JSON，用繁體中文表達。
        ),
        partial_variables={"format_instructions": format_instructions}
    )

    prompt = template.format(content=state.raw_info)

    response = llm([HumanMessage(content=prompt)])
    summary = parser.parse(response.content)
    state.summary = json.dumps(summary, indent=2, ensure_ascii=False)
    return state


def arrange_schedule_node(state: TravelState):
    parser = StrOutputParser()

    example = """
=== 第 1 天 (2025-10-10) ===
🌅 早上 08:00-12:00
- 09:00 抵達台北車站
- 10:00 前往中正紀念堂（捷運淡水信義線）
  - 參觀時間：1.5 小時
  - 門票：免費
  
🌞 中午 12:00-14:00  
- 12:30 鼎泰豐信義店用餐
  - 推薦：小籠包、炒飯
  - 預算：400-500 元/人
  
🌆 下午 14:00-18:00
- 15:00 台北 101 觀景台
  - 門票：600 元
  - 停留時間：2 小時

🌃 晚上 18:00-21:00
- 18:30 寧夏夜市晚餐
  - 推薦：豬肝湯、蚵仔煎
  - 預算：200-300 元/人

💡 當日小提醒：
- 攜帶悠遊卡方便搭乘捷運
- 台北 101 建議提前線上購票
- 預估花費：1,200-1,500 元/人
"""

    template = PromptTemplate(
        input_variables=["summary", "destination", "start_date", "end_date"],
        template="""
            你是一位專業旅遊行程規劃師，請根據以下旅遊摘要資訊：{summary}
            為旅客安排一個輕鬆合理的旅遊行程，考慮：
            - 景點之間的距離與交通時間
            - 餐廳與景點的地點搭配
            - 住宿的 check-in / check-out 時間
            - 每天行程3-4 個主要景點，不要太緊湊
            - 標註交通方式和預估時間
            f請參考以下行程格式範例：{example}
            旅遊地點：{destination}
            旅遊日期：{start_date} 至 {end_date}
            請以繁體中文輸出完整行程。"""
    )

    prompt = template.format(
        summary=state.summary,
        destination=state.destination,
        start_date=state.start_date,
        end_date=state.end_date,
        example=example
    )

    response = llm([HumanMessage(content=prompt)])
    state.schedule = parser.parse(response.content)
    return state

graph = StateGraph(TravelState)

graph.add_node("search_node", search_node)
graph.add_node("summary_node", summary_node)
graph.add_node("arrange_schedule_node", arrange_schedule_node)

graph.set_entry_point("search_node")
graph.add_edge("search_node", "summary_node")
graph.add_edge("summary_node", "arrange_schedule_node")
graph.add_edge("arrange_schedule_node", END)

app = graph.compile()

if __name__ == "__main__":
    state = TravelState(
        destination="台南",
        start_date="2025-10-24",
        end_date="2025-10-26"
    )

    final_state_dict  = app.invoke(state)
    final_state = TravelState(**final_state_dict)
    print("✅ 旅遊摘要：")
    print(final_state.summary)
    print("\n✅ 建議行程：")
    print(final_state.schedule)

