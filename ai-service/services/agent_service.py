import time

from services.trace_service import Trace
from services.router import route
from services.memory_service import resolve_context

from services.sql_service import run_sql
from services.rag_service import run_rag

from services.response_service import generate_answer
from services.chart_service import generate_chart


def run_agent(message):

    start = time.time()

    trace = Trace()

    try:

        trace.start_step("context")

        message = resolve_context(message)

        trace.end_step("context")

        trace.start_step("route")

        decision = route(message, trace=trace)

        trace.end_step("route")

        intent = decision["intent"]

        trace.add("intent", intent)

        if intent in ("sql", "chart"):

            trace.start_step("sql")

            result = run_sql(message, intent, trace=trace)

            trace.end_step("sql")

            if "error" in result:

                answer = result["error"]

                if answer == "NO_AVAILABLE_FIELD":

                    answer = "现有数据里没有这个指标，换个问法试试。"

                return {"answer": answer, "chart": None}

            data = result["data"]

            if intent == "chart":

                chart = generate_chart(data, message, trace=trace)

                if chart is None:

                    return {"answer": "没有查到数据，无法生成图表。", "chart": None}

                if "error" in chart:

                    return {"answer": chart["error"], "chart": None}

                return {"answer": "图表生成完成", "chart": chart}

            return {
                "answer": generate_answer(data, message, trace=trace),
                "chart": None
            }

        if intent == "rag":

            trace.start_step("rag")

            answer = run_rag(message, trace=trace)

            trace.end_step("rag")

            return {"answer": answer, "chart": None}

        return {
            "answer": generate_answer(None, message, trace=trace),
            "chart": None
        }

    except Exception as error:

        trace.add_error(error)

        raise error

    finally:

        trace.add("latency", round(time.time() - start, 3))

        trace.save()
