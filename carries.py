from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional, Type, List
import logging
import weakref

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
# 수정
@singleton
class DatabaseManager:
    _lock = Lock()

    def __init__(self):
        self._data = {}

    def get_data(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set_data(self, key: str, value: str) -> None:
        self._data[key] = value

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

class ShippingDecorator(ShippingStrategy):
    def __init__(self, wrapped: ShippingStrategy):
        self._wrapped = wrapped

    @abstractmethod
    def calculate_cost(self) -> float:
        pass

class InsuranceDecorator(ShippingDecorator):
    def calculate_cost(self) -> float:
        return self._wrapped.calculate_cost() + 5.00

class PriorityDecorator(ShippingDecorator):
    def calculate_cost(self) -> float:
        return self._wrapped.calculate_cost() + 10.00

class ShippingFactory:
    strategies: Dict[str, Type[ShippingStrategy]] = {
        "일반": StandardShipping,
        "익일": NextDayShipping,
        "국제": InternationalShipping
    }

    decorators: Dict[str, Type[ShippingDecorator]] = {
        "보험": InsuranceDecorator,
        "우선": PriorityDecorator
    }

    def get_shipping_strategy(self, type: str, decorator: Optional[str] = None) -> ShippingStrategy:
        try:
            strategy = self.strategies[type]()
            if decorator:
                strategy = self.decorators[decorator](strategy)
            return strategy
        except KeyError:
            raise ValueError(f"오류 발생: {type} 또는 {decorator}는 지원되지 않는 옵션입니다.")

class Subject:
    def __init__(self):
        self._observers: Dict[str, List[weakref.ref]] = {}
        self._state: Optional[str] = None

    def attach(self, observer, event_type: str) -> None:
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(weakref.ref(observer))

    def detach(self, observer, event_type: str) -> None:
        try:
            self._observers[event_type].remove(weakref.ref(observer))
        except (ValueError, KeyError):
            pass

    def notify(self, event_type: str) -> None:
        for weak_observer in self._observers.get(event_type, []):
            observer = weak_observer()
            if observer is not None:
                observer.update(self._state)

    def set_state(self, state: str, event_type: str) -> None:
        self._state = state
        self.notify(event_type)

class Observer(ABC):
    @abstractmethod
    def update(self, state: str) -> None:
        pass

class Branch(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, state: str) -> None:
        logging.info(f"{self.name} 알림: {state}")

class PackageTracker:
    def __init__(self, package_id: str):
        self.package_id = package_id
        self.history = []

    def update_status(self, status: str):
        self.history.append(status)
        logging.info(f"패키지 {self.package_id} 상태 업데이트: {status}")

    def get_history(self) -> List[str]:
        return self.history

class TrackedPackage(Subject):
    def __init__(self, package_id: str):
        super().__init__()
        self.tracker = PackageTracker(package_id)

    def set_state(self, state: str, event_type: str) -> None:
        self.tracker.update_status(state)
        self._state = state
        self.notify(event_type)

def setup_tracked_package(destination: str, shipping_type: str, package_id: str, decorator: Optional[str]) -> None:
    package = TrackedPackage(package_id)
    branch_name = destination.capitalize() + " 지점"
    branch = Branch(branch_name)
    package.attach(branch, "배송 상태")

    shipping_option = shipping_factory.get_shipping_strategy(shipping_type, decorator)
    logging.info(f"패키지 ID: {package_id} - 목적지: {destination} - 배송 유형: {shipping_type} - 택배 정보: {decorator} - 비용: {shipping_option.calculate_cost()} 원")

    package.set_state("배송 준비 완료", "배송 상태")
    package.set_state("배송 중", "배송 상태")
    package.set_state(f"{destination}에 도착", "배송 상태")
    package.set_state("배송 완료", "배송 상태")
    package.detach(branch, "배송 상태")
    
    logging.info(f"패키지 {package_id} 배송 기록: {package.tracker.get_history()}")

shipping_factory = ShippingFactory()

destinations = input('목적지를 입력해주세요: ').split()
shipping_types = input('배송 방법을 입력해주세요: ').split()
decorator = input('적용할 데코레이터를 입력해주세요 (보험/우선/없음): ')
decorator = None if decorator == "없음" else decorator

for destination in destinations:
    for shipping_type in shipping_types:
        package_id = f"{destination}_{shipping_type}_{hash(destination + shipping_type)}"
        setup_tracked_package(destination, shipping_type, package_id, decorator)