from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional, Type, List
import logging
import weakref

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 싱글턴 데코레이터
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseManager:
    """
    싱글턴 패턴을 사용하는 데이터베이스 관리자 클래스
    """
    _lock = Lock()  # 스레드 안전을 보장하기 위한 락

    def __init__(self):
        self._data = {}  # 가상 데이터베이스 초기화

    def get_data(self, key: str) -> Optional[str]:
        """
        주어진 키에 해당하는 데이터를 반환합니다.
        :param key: 데이터베이스에서 조회할 키
        :return: 키에 해당하는 데이터 값
        """
        return self._data.get(key)

    def set_data(self, key: str, value: str) -> None:
        """
        주어진 키와 값으로 데이터를 설정합니다.
        :param key: 데이터베이스에 설정할 키
        :param value: 키에 설정할 값
        """
        self._data[key] = value

class ShippingStrategy(ABC):
    """
    배송 전략을 정의하는 추상 베이스 클래스
    """
    @abstractmethod
    def calculate_cost(self) -> float:
        """
        배송 비용을 계산하는 메소드
        :return: 배송 비용
        """
        pass

class StandardShipping(ShippingStrategy):
    """
    표준 배송 전략 클래스
    """
    def calculate_cost(self) -> float:
        return 5.00

class NextDayShipping(ShippingStrategy):
    """
    익일 배송 전략 클래스
    """
    def calculate_cost(self) -> float:
        return 20.00

class InternationalShipping(ShippingStrategy):
    """
    국제 배송 전략 클래스
    """
    def calculate_cost(self) -> float:
        return 15.00

class ShippingFactory:
    """
    배송 전략을 생성하는 팩토리 클래스
    """
    strategies: Dict[str, Type[ShippingStrategy]] = {
        "일반": StandardShipping,
        "익일": NextDayShipping,
        "국제": InternationalShipping
    }

    def get_shipping_strategy(self, type: str) -> ShippingStrategy:
        """
        주어진 유형에 맞는 배송 전략 객체를 반환합니다.
        :param type: 배송 유형
        :return: 배송 전략 객체
        :raises ValueError: 지원되지 않는 배송 유형일 경우
        """
        try:
            return self.strategies[type]()
        except KeyError:
            raise ValueError(f"오류 발생: {type}는 지원되지 않는 배송 유형입니다.")

class Subject:
    """
    상태 변화를 알리는 옵저버 패턴의 주체 클래스
    """
    def __init__(self):
        self._observers: Dict[str, List[weakref.ref]] = {}  # 이벤트 유형별 옵저버 관리
        self._state: Optional[str] = None

    def attach(self, observer, event_type: str) -> None:
        """
        옵저버를 주어진 이벤트 유형에 등록합니다.
        :param observer: 등록할 옵저버
        :param event_type: 옵저버를 등록할 이벤트 유형
        """
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(weakref.ref(observer))

    def detach(self, observer, event_type: str) -> None:
        """
        주어진 이벤트 유형에서 옵저버를 제거합니다.
        :param observer: 제거할 옵저버
        :param event_type: 옵저버를 제거할 이벤트 유형
        """
        try:
            self._observers[event_type].remove(weakref.ref(observer))
        except (ValueError, KeyError):
            pass

    def notify(self, event_type: str) -> None:
        """
        주어진 이벤트 유형의 모든 옵저버에게 상태 변화를 알립니다.
        :param event_type: 상태 변화를 알릴 이벤트 유형
        """
        for weak_observer in self._observers.get(event_type, []):
            observer = weak_observer()
            if observer is not None:
                observer.update(self._state)

    def set_state(self, state: str, event_type: str) -> None:
        """
        주어진 상태로 변경하고 해당 이벤트 유형의 옵저버들에게 알립니다.
        :param state: 새로운 상태
        :param event_type: 상태 변화를 알릴 이벤트 유형
        """
        self._state = state
        self.notify(event_type)

class Observer(ABC):
    """
    옵저버 인터페이스
    """
    @abstractmethod
    def update(self, state: str) -> None:
        """
        주체의 상태 변화를 수신하여 처리합니다.
        :param state: 주체의 새로운 상태
        """
        pass

class Branch(Observer):
    """
    지점을 나타내는 클래스, 옵저버 패턴의 구현체
    """
    def __init__(self, name: str):
        self.name = name

    def update(self, state: str) -> None:
        """
        주체의 상태 변화를 로그로 기록합니다.
        :param state: 주체의 새로운 상태
        """
        logging.info(f"{self.name} 알림: {state}")

def setup_package(destination: str, shipping_type: str) -> None:
    """
    배송 옵션 및 목적지를 설정하고 처리하는 함수
    :param destination: 배송 목적지
    :param shipping_type: 배송 유형
    """
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
shipping_types = ["일반", "익일", "국제"]

for destination in destinations:
    for shipping_type in shipping_types:
        setup_package(destination, shipping_type)

# 오류 처리: 알 수 없는 배송 타입 처리
try:
    setup_package("인천", "알 수 없는 유형")
except ValueError as e:
    logging.error(e)
