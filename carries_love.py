from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional, Type

# 싱글턴 패턴을 사용하는 데이터베이스 관리자 클래스
class DatabaseManager:
    _instance = None
    _lock = Lock()  # 스레드 안전을 보장하기 위한 락

    # 객체 생성을 관리하여 단일 인스턴스만 존재하도록 함
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._data = {}  # 가상 데이터베이스 초기화
        return cls._instance

    # 데이터베이스에서 데이터를 검색하는 메소드
    def get_data(self, key):
        return self._data.get(key)

    # 데이터베이스에 데이터를 저장하는 메소드
    def set_data(self, key, value):
        self._data[key] = value

# 배송 전략을 정의하는 추상 베이스 클래스
class ShippingStrategy(ABC):

    # 배송 비용을 계산하는 추상 메소드
    @abstractmethod
    def calculate_cost(self) -> float:
        pass

# 표준 배송을 처리하는 클래스
class StandardShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 5.00

# 익일 배송을 처리하는 클래스
class NextDayShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 20.00

# 국제 배송을 처리하는 클래스
class InternationalShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 15.00

# 배송 전략을 생성하는 팩토리 클래스
class ShippingFactory:
    strategies: Dict[str, Type[ShippingStrategy]] = {
        "standard": StandardShipping,
        "nextday": NextDayShipping,
        "international": InternationalShipping
    }

    # 주어진 배송 타입에 맞는 배송 전략 객체를 생성하는 메소드
    def get_shipping_strategy(self, type: str) -> ShippingStrategy:
        try:
            return self.strategies[type]()
        except KeyError:
            raise ValueError(f"오류 발생: {type}")

# 상태 변화를 알리는 옵저버 패턴의 주체 클래스
class Subject:
    def __init__(self):
        self._observers = []  # 옵저버 목록
        self._state = None

    # 옵저버를 추가하는 메소드
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    # 옵저버를 제거하는 메소드
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    # 모든 옵저버에게 상태 변경을 알리는 메소드
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    # 상태를 설정하고 변경을 알리는 메소드
    def set_state(self, state):
        self._state = state
        self.notify()

# 옵저버 인터페이스
class Observer(ABC):
    def update(self, state):
        pass

# 지점을 나타내는 클래스, 옵저버 패턴의 구현체
class Branch(Observer):
    def __init__(self, name):
        self.name = name

    # 상태 업데이트 시 호출되는 메소드
    def update(self, state):
        print(f"{self.name} 지점 알림: {state}")

# 배송 옵션 및 목적지를 설정하고 처리하는 함수
def setup_package(destination, shipping_type):
    package = Subject()
    branch_name = destination.capitalize() + " 지점"
    branch = Branch(branch_name)
    package.attach(branch)

    shipping_option = shipping_factory.get_shipping_strategy(shipping_type)
    print(f"목적지: {destination} - 배송 유형: {shipping_type} - 비용: {shipping_option.calculate_cost()} 원")

    package.set_state("배송 준비 완료")
    package.set_state("배송 중")
    package.set_state(destination + "에 도착")
    package.detach(branch)
    package.set_state("배송 완료")

# 전역 변수로 팩토리 인스턴스를 초기화
shipping_factory = ShippingFactory()

# 예제 실행: 다양한 목적지와 배송 옵션을 사용
destinations = ["용인", "서울", "부산"]
shipping_types = ["standard", "nextday", "international"]

for destination in destinations:
    for shipping_type in shipping_types:
        setup_package(destination, shipping_type)

# 오류 처리: 알 수 없는 배송 타입 처리
try:
    setup_package("Incheon", "다시 선택해주십시오.")
except ValueError as e:
    print(e)
