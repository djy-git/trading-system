# base-structure
Machine learning project에 사용될 수 있는 기본 구조


# I. Directory structure

```
ROOT
├── LICENSE
├── README.md
├── log
│   └── 22-01-01_19-58-09.log
├── playground
│   └── main.py
└── base_structure
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

# II. File description
## 1. `/common`: Commonly used modules

```
> Dependency between modules

env.py ── LoggerFactory.py ─┬─ DBHandler.py     ─┬─ util.py 
                            ├─ SignalHandler.py ─┤ 
                            ├─ Timer.py         ─┤ 
                            └─ config.py        ─┘
```

- `env.py`: 자주 사용되는 package, function, class, constants 등을 정의하는 module 
  - 가장 하위 module로 **project의 다른 module을 import하면 안 됨(circular reference)**
- `LoggerFactory.py`: Logger를 생성하기 위한 class(singleton)
- `DBHandler.py`: DB에 접근하기 위한 class(singleton)
- `SignalHandler.py`: Signal handler를 관리하는 class 
- `Timer.py`: 수행하는 작업의 시간을 측정할 수 있는 class
- `config.py`: 공개적으로 관리할 수 있는 parameter 값들이 저장되는 script
- `util.py`: 이상의 module들을 import 하고 추가적으로 function, class, constants 등을 정의하는 module
  - `from common.util import *` 로 `common` 내 모든 module들을 import 할 수 있음


# III. Remarks
## 1. `PATH`
- `/common/env.py`에서 `PATH`를 정의하는 부분을 참고

## 2. `LOGGER`
- `/common/LoggerFactory.py`에서 `LOGGER`를 정의하는 부분을 참고
- 편의를 위해 **global variable**로 선언되어 있으므로 사용에 주의가 필요
- `LOGGER.info()`, `LOGGER.exception()` 등 사용가능
- `PATH.LOG_FILE`에 저장
- `@L`을 사용하여 자동적으로 code level과 소요 시간을 추적할 수 있음
  - 자세한 내용은 `/common/util.py`에서 `L`을 정의하는 부분을 참고
  ```
    @L
    def F():
      G()
  
    @L
    def G():
      pass
  
    F()
  ```

  ```  
    > 1               F()
    > 1.1             G()
    * 1.1             [0.00s]
    * 1               [0.00s]
  ```

## 3. `DBHandler`
- `/common/DBHandler.py`에서 `DBHandler`를 정의하는 부분을 참고
- Singleton pattern으로 정의되어 하나의 객체만을 생성
- 여러 개의 connection에 대하여 각각 하나의 connection 만을 생성
  - 자세한 내용은 [Multi Database Handler (Singleton)](https://djy-git.github.io/2021/12/15/dbhandler.html) 참조
- `PATH.INI_FILE`에 기록된 계정 정보를 사용하여 DB에 접근하는 것을 권장
  - `/common/util.py`에 정의된 `ini2dict()`를 사용하여 `db_info`를 읽어올 수 있음

## 4. `SignalHandler`
- `/common/SignalHandler.py`에서 `SignalHandler`를 정의하는 부분을 참고
- `signal` module에 정의된 signal을 처리할 수 있음

## 5. `Timer`
- `/common/Timer.py`에서 `Timer`를 정의하는 부분을 참고
  ```
  def fn():
    # do something
  
  
  # Usage 1 (context manager)
  with Timer("fn()"):
    fn()
  
  
  # Usage 2 (decorator)
  @Timer("fn()")
  def fn():
    # do something
  ```
