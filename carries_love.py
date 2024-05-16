from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional, Type, List
import logging
import weakref
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

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

    @abstractmethod
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        pass

    @abstractmethod
    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        pass

class StandardShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 5.00

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=2, hours=0)

class NextDayShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 20.00

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=1, hours=0)

class InternationalShipping(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 15.00

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=7, hours=0)

class ShippingDecorator(ShippingStrategy):
    def __init__(self, wrapped: ShippingStrategy):
        self._wrapped = wrapped

    @abstractmethod
    def calculate_cost(self) -> float:
        pass

    @abstractmethod
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        pass

    @abstractmethod
    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        pass

class InsuranceDecorator(ShippingDecorator):
    def calculate_cost(self) -> float:
        return self._wrapped.calculate_cost() + 5.00

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        return self._wrapped.get_delivery_steps(destination, origin, departure_time)

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return self._wrapped.calculate_arrival_time(departure_time)

class PriorityDecorator(ShippingDecorator):
    def calculate_cost(self) -> float:
        return self._wrapped.calculate_cost() + 10.00

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        return self._wrapped.get_delivery_steps(destination, origin, departure_time)

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return self._wrapped.calculate_arrival_time(departure_time)

class CompanyStrategy(ShippingStrategy):
    def calculate_cost(self) -> float:
        return 0.00

    @abstractmethod
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        pass

    @abstractmethod
    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        pass

class Hanjin(CompanyStrategy):
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", f"{destination}에 {arrival_time}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=3, hours=3)

class Logen(CompanyStrategy):
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["택배 발송", f"{origin}에서 출발", f"{destination}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=2, hours=2)

class PostOffice(CompanyStrategy):
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["접수", f"{arrival_time} 도착 예정", f"{destination}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=1, hours=2)

class CJ(CompanyStrategy):
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["접수", "방금 출발", "지금 배송 중", "오늘 도착 예정", f"{destination}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=2, hours=5)

class Lotte(CompanyStrategy):
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["배송 준비 완료", "배송 중", f"{destination}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=3, hours=12)

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

    companies: Dict[str, Type[CompanyStrategy]] = {
        "한진": Hanjin,
        "로젠": Logen,
        "우체국": PostOffice,
        "CJ": CJ,
        "롯데": Lotte
    }

    def get_shipping_strategy(self, type: str, decorator: Optional[str] = None, company: Optional[str] = None) -> ShippingStrategy:
        try:
            if company:
                strategy = self.companies[company]()
            else:
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

def setup_tracked_package(destination: str, origin: str, departure_time: datetime, shipping_type: str, package_id: str, decorator: Optional[str], company: Optional[str]) -> None:
    package = TrackedPackage(package_id)
    branch_name = destination.capitalize() + " 지점"
    branch = Branch(branch_name)
    package.attach(branch, "배송 상태")

    shipping_option = shipping_factory.get_shipping_strategy(shipping_type, decorator, company)
    arrival_time = shipping_option.calculate_arrival_time(departure_time)
    logging.info(f"패키지 ID: {package_id} - 목적지: {destination} - 출발지: {origin} - 출발 시간: {departure_time} - 도착 시간: {arrival_time} - 배송 유형: {shipping_type} - 데코레이터: {decorator} - 택배 회사: {company} - 비용: {shipping_option.calculate_cost()} 원")

    steps = shipping_option.get_delivery_steps(destination, origin, departure_time)
    for step in steps:
        package.set_state(step, "배송 상태")
    package.detach(branch, "배송 상태")

    logging.info(f"패키지 {package_id} 배송 기록: {package.tracker.get_history()}")

shipping_factory = ShippingFactory()

# 목적지와 출발지, 출발 시간, 배송 방법, 데코레이터, 택배 회사 선택
origin = input('출발지를 입력해주세요: ').strip()
destination = input('목적지를 입력해주세요: ').strip()
departure_time_str = input('출발 시간을 입력해주세요 (예: 2024-05-18 14:30): ').strip()
departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M')
shipping_type = input('배송 방법을 입력해주세요 (일반/익일/국제): ').strip()
decorator = input('적용할 데코레이터를 입력해주세요 (보험/우선/없음): ').strip()
decorator = None if decorator == "없음" else decorator
company = input('택배 회사를 선택해주세요 (한진/로젠/우체국/CJ/롯데): ').strip()

# 패키지 ID 생성 및 설정
package_id = f"{destination}_{origin}_{departure_time_str}_{shipping_type}_{company}_{hash(destination + origin + departure_time_str + shipping_type + company)}"
setup_tracked_package(destination, origin, departure_time, shipping_type, package_id, decorator, company)
