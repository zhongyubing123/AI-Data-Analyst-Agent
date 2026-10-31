import json
import sys
import os
import time


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


sys.path.append(
    os.path.join(
        BASE_DIR,
        "ai-service"
    )
)


from services.agent_service import run_agent



TEST_FILE = os.path.join(
    os.path.dirname(__file__),
    "rag_cases.json"
)



RESULT_FILE = os.path.join(
    os.path.dirname(__file__),
    "rag_results.json"
)



def load_cases():

    with open(
        TEST_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)



def evaluate_case(case):


    start=time.time()


    try:

        response = run_agent(
            case["question"]
        )


        text=str(response)


        keyword = case[
            "expected_keyword"
        ]


        success = keyword in text



        return {

            "id":
                case["id"],

            "question":
                case["question"],

            "success":
                success,

            "keyword":
                keyword,

            "latency":
                round(
                    time.time()-start,
                    3
                ),

            "response":
                text

        }


    except Exception as e:


        return {

            "id":
                case["id"],

            "success":
                False,

            "error":
                str(e)

        }



def main():


    cases=load_cases()


    results=[]


    for case in cases:

        result=evaluate_case(case)

        print(result)

        results.append(result)



    total=len(results)


    success=sum(
        1
        for r in results
        if r["success"]
    )


    summary={

        "total":
            total,

        "success":
            success,

        "accuracy":
            round(
                success/total,
                3
            ),

        "results":
            results

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



    print("================")
    print(summary)



if __name__=="__main__":

    main()