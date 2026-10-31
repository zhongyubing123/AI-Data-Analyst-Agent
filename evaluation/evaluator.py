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

MODE = os.getenv("MODE", "full")


# 指定用例文件，不指定就按 MODE 走默认的两份
CASES = os.getenv("CASES", "")



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



if CASES:

    TEST_FILE=os.path.join(
        os.path.dirname(__file__),
        CASES
    )

elif MODE=="fast":

    TEST_FILE=os.path.join(
        os.path.dirname(__file__),
        "fast_test_cases.json"
    )

else:

    TEST_FILE=os.path.join(
        os.path.dirname(__file__),
        "agent_test_cases.json"
    )


RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "results"
)

os.makedirs(RESULTS_DIR, exist_ok=True)

CASE_STEM = os.path.splitext(
    os.path.basename(TEST_FILE)
)[0]

RESULT_FILE = os.path.join(
    RESULTS_DIR,
    f"{MODE}_{CASE_STEM}_results.json"
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

    """fast 模式只验证语句生成，其他类型跳过。"""

    if case["type"] not in ("sql", "sql_retry"):

        return {"answer": "skip"}

    return {"sql": generate_sql(case.get("question"))}



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



    # 表名断言只对 fast 模式有意义：那个模式响应就是 SQL 文本。
    # full 模式返回自然语言，不会出现表名。
    table=expected.get(
        "table"
    )


    if table and MODE == "fast":

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