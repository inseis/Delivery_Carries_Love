from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional, Type
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 싱글턴 패턴을 사용하는 데이터베이스 관리자 클래스
class DatabaseManager:
    _instance = None
    _lock = Lock()  # 스레드 안전을 보장하기 위한 락

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._data = {}  # 가상 데이터베이스 초기화
        return cls._instance

    def get_data(self, key):
        return self._data.get(key)

    def set_data(self, key, value):
        self._data[key] = value

# 배송 전략을 정의하는 추상 베이스 클래스
class ShippingStrategy(ABC):

    @abstractmethod
    def calculate_cost(self) -> float:
        pass

class StandardShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 5.00

class NextDayShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 20.00

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

    def get_shipping_strategy(self, type: str) -> ShippingStrategy:
        try:
            return self.strategies[type]()
        except KeyError:
            raise ValueError(f"오류 발생: {type}는 지원되지 않는 배송 유형입니다.")

# 상태 변화를 알리는 옵저버 패턴의 주체 클래스
class Subject:
    def __init__(self):
        self._observers = {}  # 이벤트 유형별 옵저버 관리
        self._state = None

    def attach(self, observer, event_type):
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def detach(self, observer, event_type):
        try:
            self._observers[event_type].remove(observer)
        except (ValueError, KeyError):
            pass

    def notify(self, event_type):
        for observer in self._observers.get(event_type, []):
            observer.update(self._state)

    def set_state(self, state, event_type):
        self._state = state
        self.notify(event_type)

# 옵저버 인터페이스
class Observer(ABC):
    @abstractmethod
    def update(self, state):
        pass

# 지점을 나타내는 클래스, 옵저버 패턴의 구현체
class Branch(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, state):
        logging.info(f"{self.name} 지점 알림: {state}")

# 배송 옵션 및 목적지를 설정하고 처리하는 함수
def setup_package(destination, shipping_type):
    package = Subject()
    branch_name = destination.capitalize() + " 지점"
    branch = Branch(branch_name)
    package.attach(branch, "배송 시작")

    shipping_option = shipping_factory.get_shipping_strategy(shipping_type)
    logging.info(f"목적지: {destination} - 배송 유형: {shipping_type} - 비용: {shipping_option.calculate_cost()} 원")

    package.set_state("배송 준비 완료", "배송 시작")
    package.set_state("배송 중", "배송 중")
    package.set_state(destination + "에 도착", "배송 도착")
    package.detach(branch, "배송 도착")
    package.set_state("배송 완료", "배송 완료")

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
    setup_package("Incheon", "unknown_type")
except ValueError as e:
    logging.error(e)
