import asyncio
import pyvts

async def connect_auth(myvts):
    await myvts.connect()
    await myvts.request_authenticate_token()
    await myvts.request_authenticate()
    await myvts.close()

async def trigger(myvts, feeling):
    await myvts.connect()
    await myvts.request_authenticate()
    response_data = await myvts.request(myvts.vts_request.requestHotKeyList())
    # print(response_data)
    hotkey_list = []
    for hotkey in response_data["data"]["availableHotkeys"]:
        hotkey_list.append(hotkey["name"])
    # print(hotkey_list)
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(feeling)
    await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'
    await myvts.close()

def extract_movement(text):
    # 찾은 괄호 안의 내용을 저장할 리스트
    feelings = []

    # 괄호 안의 내용을 찾기
    matches = text.findall(r'\((.*?)\)', text)

    # 찾은 내용을 리스트에 추가
    for match in matches:
        feelings.append(match)

    # 원본 문장에서 괄호와 내용 제거
    text = text.sub(r'\(.*?\)', '', text)

    return feelings, text

if __name__ == "__main__":
    myvts = pyvts.vts()
    try:
        text = "여러분, 기체 분자 운동론에 대한 설명, 어떠셨나요? 여기까진 이해가 되셨을까요? 이해가 되지 않는 부분이 있다면, 질문을 통해 함께 해결해봅시다. (음미)"
        extract_movement(text)
        asyncio.run(connect_auth(myvts))
        asyncio.run(trigger(myvts, text))
    except:
        print()