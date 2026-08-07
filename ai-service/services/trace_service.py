import time
import json
import os

from datetime import datetime



class Trace:


    def __init__(self):

        self.data = {

            "start_time":
                time.time(),

            "steps": {},

            "token_usage": {

                "prompt_tokens":0,

                "completion_tokens":0,

                "total_tokens":0

            },

            "error":None

        }



    def add(
        self,
        key,
        value
    ):

        self.data[key]=value



    def start_step(self,name):

        self.data[
            "_step_start_"+name
        ] = time.time()



    def end_step(self,name):

        start = self.data.get(
            "_step_start_"+name
        )


        if start:

            self.data["steps"][name] = round(
                time.time()-start,
                3
            )



    def add_token(self,usage):

        if usage:

            self.data["token_usage"] = {

                "prompt_tokens":
                    usage.get(
                        "prompt_tokens",
                        0
                    ),

                "completion_tokens":
                    usage.get(
                        "completion_tokens",
                        0
                    ),

                "total_tokens":
                    usage.get(
                        "total_tokens",
                        0
                    )

            }



    def add_error(self,error):

        self.data["error"] = str(error)



    def save(self):


        self.data["latency"] = round(
            time.time()
            -
            self.data["start_time"],
            3
        )



        keys = [

            k for k in self.data

            if k.startswith(
                "_step_start"
            )

        ]


        for k in keys:

            del self.data[k]



        os.makedirs(
            "logs",
            exist_ok=True
        )



        filename = datetime.now().strftime(
            "logs/trace_%Y%m%d_%H%M%S.json"
        )


        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                self.data,
                f,
                ensure_ascii=False,
                indent=4,
                default=str
            )