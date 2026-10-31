from pathlib import Path
import time
import json

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

            "error":None,
            "llm_calls": 0

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



    def add_token(self, usage):

        if not usage:
            return

        self.data["llm_calls"] = self.data.get("llm_calls", 0) + 1

        for key in (
            "prompt_tokens",
            "completion_tokens",
            "total_tokens"
        ):

            self.data["token_usage"][key] += int(
                usage.get(key) or 0
            )



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



        log_dir = Path(__file__).resolve().parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        filename = log_dir / datetime.now().strftime(
            "trace_%Y%m%d_%H%M%S_%f.json"
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