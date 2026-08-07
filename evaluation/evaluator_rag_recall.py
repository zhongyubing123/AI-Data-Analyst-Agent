import json
import os
import sys
import time


# 添加 ai-service路径
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


AI_SERVICE_PATH = os.path.join(
    BASE_DIR,
    "ai-service"
)


sys.path.append(
    AI_SERVICE_PATH
)


from services.vector_search import search



TEST_FILE = os.path.join(
    os.path.dirname(__file__),
    "rag_test_cases.json"
)


RESULT_FILE = os.path.join(
    os.path.dirname(__file__),
    "rag_recall_results.json"
)



def load_cases():

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def evaluate_case(case):


    print("\n================")

    print(
        "问题:",
        case["question"]
    )


    start=time.time()


    try:


        # 直接测试FAISS召回
        docs = search(
            case["question"],
            top_k=3
        )


        hit=False


        matched_doc=[]


        for doc in docs:


            if case["expected"] in doc:

                hit=True

                matched_doc.append(doc)



        latency=round(
            time.time()-start,
            3
        )


        result={

            "id":case["id"],

            "question":
                case["question"],

            "success":
                hit,

            "expected":
                case["expected"],

            "retrieved_docs":
                docs,

            "matched_docs":
                matched_doc,

            "latency":
                latency
        }



    except Exception as e:


        result={

            "id":case["id"],

            "question":
                case["question"],

            "success":
                False,

            "error":
                str(e)
        }



    print(result)


    return result




def main():


    cases=load_cases()


    results=[]


    for case in cases:


        results.append(
            evaluate_case(case)
        )



    total=len(results)


    hit=sum(

        1

        for r in results

        if r["success"]

    )



    recall=round(

        hit/total,

        3

    )



    summary={


        "total":
            total,


        "hit":
            hit,


        "recall":
            recall,


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



    print("\n==========")

    print(

        "RAG Recall:",

        recall

    )



if __name__=="__main__":

    main()