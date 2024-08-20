# voice_assistant.py
import streamlit as st
import speech_recognition as sr
import requests
from urllib.parse import quote

def main():
    st.title("음성 인식 보조")

    # 음성 인식 시작 버튼
    if st.button("음성 인식 시작"):
        # 음성 인식 객체 생성
        r = sr.Recognizer()

        with sr.Microphone() as source:
            st.write("말씀해 주세요...")
            audio = r.listen(source)

        try:
            # Google Speech Recognition을 사용하여 음성을 텍스트로 변환
            text = r.recognize_google(audio, language="ko-KR")
            st.write("인식된 텍스트:", text)

            # Flask 서버에 텍스트 전송
            response = requests.post("http://localhost:5000/api/searchMovie", json={"userRequest": {"utterance": text}})
            result = response.json()

            if 'listCard' in result['template']['outputs'][0]:
                list_card = result['template']['outputs'][0]['listCard']
                st.subheader(list_card['header']['title'])
                for item in list_card['items']:
                    st.write(f"주차장명: {item['title']}")

                    # 주소 부분을 가져와서 URL 인코딩
                    address = item['description'].split("\n")[0].split(": ")[1]
                    encoded_address = quote(address)
                    map_link = f"https://map.kakao.com/link/search/{encoded_address}"

                    st.write(f"[지도 보기]({map_link})")
                    st.write("")  # 빈 줄 추가
            else:
                st.write("주차장 정보를 찾을 수 없습니다.")

        except sr.UnknownValueError:
            st.write("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            st.write(f"음성 인식 서비스 오류: {e}")

if __name__ == "__main__":
    main()