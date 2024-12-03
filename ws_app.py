import asyncio
import threading

import websockets

from applications.ai.gpt_synthetic_path import chatbot

lock = threading.Lock()


def gpt(question):
    parts = question.split("greate ai nano enzymes#")

    if len(parts) == 2 and len(parts[1]) < 50:
        question = parts[1]
        parts = question.split("demo#")
        if len(parts) == 2:
            # How to synthesize Pd@Pt?
            answer = "To prepare Pd@Au bimetallic nanoplates with different Au/Pd ratios, 0.1 mL of the synthesized Pd NSs stock solution (1.2 mg mL-1) and different masses (e.g., 0.5, 1, 2, 3.5, and 5 mg) of AuPPh3Cl (2 mg mL−1 in DMF) were mixed in DMF, respectively. Then hydrazine (80%, 100 µL) was added dropwise while the mixture was stirred vigorously. After all the above steps were completed, the solution was left undisturbed at room temperature for more than 12 h. The products were precipitated by acetone, separated via centrifugation, and further purified by an ethanol–acetone mixture. The resulting solution was stored at 4 °C for future use. In the case of Pd@Pt bimetallic nanoplates with different Pt/Pd ratios, a similar procedure was applied except that a different mass of Pt(acac)2 (2 mg mL−1 in DMF) was used to replace AuPPh3Cl, and the solution was left undisturbed at 100 °C for more than 12 h. The amounts of Pd, Au, and Pt were also measured by ICP-MS (the mass ratios of Au/Pd from a to e are 1.5:1, 2.4:1, 3.2:1, 7.0:1, and 8.2:1, respectively; the mass ratios of Pt/Pd from a to e are 1.3:1, 2.9:1, 5:1, 8:1, and 12:1, respectively)."
        else:
            # 获取线程锁
            lock.acquire(timeout=120)
            try:
                print(question)
                answer, initial_context, past_user_messages = chatbot(question)
                print(answer)
            except Exception as e:
                print(e)
                pass
            finally:
                lock.release()

    return answer


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            await websocket.send(gpt(message))
            await websocket.close()
        except:
            pass


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8939):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    # gpt('greate ai nano enzymes#How to synthesize Pd@Pt NPS?')
    asyncio.run(main())
