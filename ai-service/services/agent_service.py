import time

from services.trace_service import Trace
from services.planner_service import planner
from services.memory_service import resolve_context

from services.sql_service import run_sql
from services.rag_service import run_rag

from services.response_service import generate_answer
from services.chart_service import generate_chart



def run_agent(message):


    start = time.time()

    trace = Trace()



    try:


        trace.start_step(
            "context"
        )


        message = resolve_context(
            message
        )


        trace.end_step(
            "context"
        )



        trace.start_step(
            "planner"
        )


        planner_result = planner(
            message
        )


        trace.end_step(
            "planner"
        )



        intent = planner_result.get(
            "intent",
            "chat"
        )



        trace.add(
            "intent",
            intent
        )



        if intent in [
            "sql",
            "chart"
        ]:


            result = run_sql(
                message,
                intent
            )


            if "error" in result:

                return {

                    "answer":
                    result["error"],

                    "chart":None

                }



            data = result["data"]



            if intent == "chart":


                return {

                    "answer":
                    "图表生成完成",

                    "chart":
                    generate_chart(
                        data,
                        message
                    )

                }



            return {

                "answer":
                generate_answer(
                    data,
                    message
                ),

                "chart":None

            }




        if intent == "rag":


            return {

                "answer":
                run_rag(message),

                "chart":None

            }




        return {

            "answer":
            generate_answer(
                None,
                message
            ),

            "chart":None

        }



    except Exception as e:


        trace.add_error(e)

        raise e



    finally:


        trace.add(
            "latency",
            round(
                time.time()-start,
                3
            )
        )


        trace.save()