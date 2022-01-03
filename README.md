# 자동 매매 시스템
데이터 수집부터 투자, 모니터링까지 자동화된 시스템을 구축하는 프로젝트


# I. Structure
```
.
├── LICENSE
├── README.md
├── algorithm
│   ├── Database\ \355\205\214\354\235\264\353\270\224\ \354\240\225\354\235\230\354\204\234.xlsx
│   ├── WBS.xlsx
│   ├── sequence\ diagram
│   │   ├── seq\ diagram\ -\ data\ collection.png
│   │   ├── seq\ diagram\ -\ data\ collection.puml
│   │   ├── seq\ diagram\ -\ invest.png
│   │   └── seq\ diagram\ -\ invest.puml
│   └── \355\224\204\353\241\234\354\240\235\355\212\270\ \354\204\244\352\263\204\353\217\204.pptx
├── docs
│   └── README.md
├── setup.py
└── trading_system
    ├── Collector
    │   └── Collector.py
    ├── Engine
    │   ├── Engine.py
    │   ├── Engine_J.py
    │   ├── Engine_L.py
    │   └── Engine_Y.py
    ├── Interface.py
    ├── Investor
    │   └── Investor.py
    ├── common
    │   ├── DBHandler.py
    │   ├── LoggerFactory.py
    │   ├── SignalHandler.py
    │   ├── Timer.py
    │   ├── account.ini
    │   ├── config.py
    │   ├── env.py
    │   └── util.py
    └── main.py
```

## 1. `algorithm`
프로젝트 설계 및 알고리즘 관련 파일들이 포함된 directory

## 2. `docs`
[sphinx](https://www.sphinx-doc.org/en/master/)를 이용한 문서화 관련 파일들이 포함된 directory

## 3. `setup.py`
Package 배포에 필요한 setup file

## 4. `trading_system`
Source code directory

### 4.1 `Collector`
데이터 수집 class

### 4.2 `Engine`
작업을 수행하는 알고리즘이 구현된 class

### 4.3 `Interface`
외부에서 각 module(`Collector`, `Investor` 등)에 접근하기 하는데 사용되는 interface class

### 4.4 `common`
Module들에서 자주 사용되는 module들을 모아놓은 package

### 4.5 `main.py`
프로그램의 시작지점
