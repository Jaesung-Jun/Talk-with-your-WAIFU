import json
import os
import openai
import time
import logging

# httpcore의 로거를 가져와서 로그 레벨을 WARNING으로 설정
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
# 만약 모든 디버그 로그를 비활성화하고 싶다면 아래 코드 사용
# logging.basicConfig(level=logging.WARNING)

# API_KEY = ""  # 원하는 URL
# ASSISTANT_ID = ""
# openai.api_key = API_KEY

class API:
    def __init__(self, assistant_id):
        self.THREAD_ID=self.create_new_thread().id
        self.assistant_id = assistant_id

    def create_new_thread(self):
        thread=openai.beta.threads.create()
        return thread

    def summit_message(self, assistant_id, thread_id, user_message):
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        run=openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        return run

    def wait_on_run(self, run, thread):
        while run.status == "queued" or run.status=="in_progress":
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread,
                run_id=run.id
            )
            time.sleep(0.2)

    def get_response(self, thread_id):
        return openai.beta.threads.messages.list(thread_id=thread_id, order="desc").data[0]

    def get_only_message(self, response):
        return response.content[0].text.value

    def show_json(self, obj):
        print(json.loads(obj.model_dump_json()))

    def get_serifu_from_message(self, user_message):
        
        run=self.summit_message(self.assistant_id, self.THREAD_ID, user_message)
        
        # Wait for response
        self.wait_on_run(run, self.THREAD_ID)

        response = self.get_response(self.THREAD_ID)
        msg_from_waifu = self.get_only_message(response)
        # print("USER REQUEST : ", user_message)
        print("WAIFU SAID : ", msg_from_waifu.split("\n")[0])
        print("WAIFU SAID (translated) : ", "".join(msg_from_waifu.split("\n")[1:]))
        return msg_from_waifu