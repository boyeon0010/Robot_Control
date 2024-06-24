# Mirobot API
## 1. Mirobot 설정
1. [Mirobot 드라이버 설치](https://www.wlkata.com/pages/download-center)
   <img width="80%" src="https://user-images.githubusercontent.com/89232601/228711820-224590ed-dfb3-4339-85db-ffd26e1ca3d5.JPG"/>

2. Mirobot과 PC 연결 후 장치관리자에서 포트 번호 확인(CH340)
   <img width="80%" src="https://user-images.githubusercontent.com/89232601/228714070-c5c13708-d18a-483d-8446-4f42f33b6c1b.JPG"/>

## 2. 가상환경 설정
1. python 3.8 버전 설치 필요
2. 터미널에 `python -m venv venv` 명령어 입력(가상환경 생성)
3. 가상환경 실행
   1. 윈도우 : `venv\Scripts\activate`
   2. 리눅스, 맥 : `source venv/bin/activate`
<img width="80%" src="https://user-images.githubusercontent.com/89232601/228713185-62edffe2-7ca8-4871-ac10-f6c6f6752210.JPG"/>

1. 다음 명령어로 라이브러리 설치
```
pip3 install -r requirements.txt
```

## 3. 실행 환경 설정
1. mirobotApi\instance\config.py 파일 생성 후 다음 정보 입력 필요
```python
PORTNAME :str = "Your Mirobot PORT" --> 미로봇 시리얼 포트
HOST :str = "Your IP ADDRESS" --> Unity Device의 IP 주소
PORT :int = "Your PORT" --> Unity Device의 포트
```

키보드 제어 실행 명령어
```
python run.py keyboard
```

컨트롤러(원격) 제어 실행 명령어
```
python run.py controller
```
