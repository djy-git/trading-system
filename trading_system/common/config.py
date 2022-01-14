"""**Configuration 변수들이 정의되는 module**

1. Constant는 대문자

----
"""

'''
참고) 증권사별 수수료 비교
https://dudrms606.tistory.com/770
https://jhshjs.tistory.com/113
'''
TAX_RATE_KR = 0.230/100  # 증권거래세               : 매도 금액에 적용 (KOSPI(2022): 0.23%)
FEE_RATE_KR = 0.015/100  # 위탁수수료 + 유관기관수수료: 매수/매도 금액에 적용 (나무(2022): 0.01%, 유관기관수수료: 0.005%)

ANNUALIZATION_FACTOR = 252
