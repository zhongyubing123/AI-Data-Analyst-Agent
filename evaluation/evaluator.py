import json
import sys
import os
import time


# =====================
# Evaluation模式
# =====================

# fast:
#   低成本测试
#
# full:
#   完整Agent测试

MODE = "full"



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


AI_SERVICE_PATH = os.path.join(
    BASE_DIR,
    "ai-service"
)


sys.path.append(AI_SERVICE_PATH)



# 完整Agent
from services.agent_service import run_agent


# fast模式需要
from services.sql_generator import generate_sql



if MODE=="fast":

    TEST_FILE=os.path.join(
        os.path.dirname(__file__),
        "fast_test_cases.json"
    )

else:

    TEST_FILE=os.path.join(
        os.path.dirname(__file__),
        "agent_test_cases.json"
    )


RESULT_FILE = os.path.join(
    os.path.dirname(__file__),
    "agent_results.json"
)



def load_test_cases():

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# =====================
# Fast Evaluation
# =====================

def fast_evaluate(case):

    """
    低成本Evaluation

    不经过完整Agent
    """

    question = case.get(
        "question"
    )


    result = {}



    # SQL测试

    if case["type"] == "sql":


        sql = generate_sql(
            question
        )


        result = {

            "sql":sql

        }



    # SQL Retry
    elif case["type"] == "sql_retry":


        sql = generate_sql(
            question
        )


        result = {

            "sql":sql

        }



    # Chat无需测试LLM
    elif case["type"] == "chat":


        result = {

            "answer":
                "skip"

        }


    # Memory暂时full测试
    elif case["type"] == "memory":


        response = run_agent(
            case["conversation"][0]
        )


        response = run_agent(
            case["conversation"][1]
        )


        result = response



    # RAG暂时跳过
    elif case["type"] == "rag":


        result = {

            "rag":
                "skip"

        }



    # Chart暂时full

    elif case["type"] == "chart":


        result = run_agent(
            question
        )



    return result




# =====================
# 判断结果
# =====================


def check_expected(case,response):

    text=str(response)


    expected=case.get(
        "expected",
        {}
    )


    keywords=expected.get(
        "keywords",
        []
    )


    for keyword in keywords:

        if keyword not in text:

            return False



    table=expected.get(
        "table"
    )


    if table:

        if table not in text:

            return False



    return True




# =====================
# 单个测试
# =====================


def evaluate_case(case):


    print("\n================")

    print(
        "测试:",
        case.get("question")
        or
        case.get("conversation")
    )


    start=time.time()


    try:


        if MODE == "full":


            if case["type"]=="memory":


                response=None


                for msg in case["conversation"]:

                    response=run_agent(msg)


            else:


                response=run_agent(
                    case["question"]
                )



        else:


            response=fast_evaluate(
                case
            )



        success=check_expected(
            case,
            response
        )



        result={

            "id":case["id"],

            "type":case["type"],

            "mode":MODE,

            "success":success,

            "latency":
                round(
                    time.time()-start,
                    3
                ),

            "response":
                str(response)

        }



    except Exception as e:


        result={

            "id":case["id"],

            "type":case["type"],

            "mode":MODE,

            "success":False,

            "error":
                str(e)

        }



    print(result)


    return result




# =====================
# 主程序
# =====================


def main():


    cases=load_test_cases()


    results=[]


    for case in cases:


        results.append(
            evaluate_case(case)
        )



    total=len(results)


    success=sum(
        1
        for r in results
        if r.get("success")
    )



    summary={

        "mode":MODE,

        "total":total,

        "success":success,

        "accuracy":
            round(
                success/total,
                3
            ),

        "results":results

    }



    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            summary,
            f,
            ensure_ascii=False,
            indent=4
        )



    print("\n================")

    print(
        "Evaluation完成"
    )

    print(summary)




if __name__=="__main__":

    main()