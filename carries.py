from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, Optional, Type, List
import weakref
from datetime import datetime, timedelta
#승환
# 싱글톤 데코레이터
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

# 데이터베이스 매니저 싱글톤 클래스
@singleton
class DatabaseManager:
    _lock = Lock()

    def __init__(self):
        self._data = {}

    def get_data(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set_data(self, key: str, value: str) -> None:
        self._data[key] = value

# 배송 전략 추상 클래스
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        pass

    @abstractmethod
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        pass

    @abstractmethod
    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        pass

# 일반 배송 전략
class StandardShipping(ShippingStrategy):
    def weight_based_fee(self, weight: float) -> float:
        if weight <= 5:
            return 0
        elif weight <= 10:
            return 2000
        else:
            return 5000 + (weight - 10) * 100

    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        base_cost = 5000
        weight_cost = self.weight_based_fee(item_weight)
        return base_cost + weight_cost

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=2, hours=0)

# 익일 배송 전략
class NextDayShipping(ShippingStrategy):
    def weight_based_fee(self, weight: float) -> float:
        if weight <= 5:
            return 0
        elif weight <= 10:
            return 2000
        else:
            return 5000 + (weight - 10) * 100
    
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        base_cost = 20000
        weight_cost = self.weight_based_fee(item_weight)
        return base_cost + weight_cost

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=1, hours=0)

# 국제 배송 전략
class InternationalShipping(ShippingStrategy):
    def weight_based_fee(self, weight: float) -> float:
        if weight <= 5:
            return 0
        elif weight <= 10:
            return 2000
        else:
            return 5000 + (weight - 10) * 100

    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        base_cost = 15000
        weight_cost = self.weight_based_fee(item_weight)
        return base_cost + weight_cost

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=7, hours=0)

# 배송 데코레이터 추상 클래스
class ShippingDecorator(ShippingStrategy):
    def __init__(self, wrapped: ShippingStrategy):
        self._wrapped = wrapped

    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return self._wrapped.calculate_cost(item_value, destination_country, item_weight)

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        return self._wrapped.get_delivery_steps(destination, origin, departure_time)

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return self._wrapped.calculate_arrival_time(departure_time)

# 보험 데코레이터 클래스
class InsuranceDecorator(ShippingDecorator):
    def calculate_cost(self, item_value: float, item_weight: float = 0) -> float:
        insurance_cost = item_value * 0.1  # 상품 가격의 10%를 보험료로 계산
        return super().calculate_cost(item_value, "", item_weight) + insurance_cost

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        return super().get_delivery_steps(destination, origin, departure_time)

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return super().calculate_arrival_time(departure_time)

# 택배 회사 전략 추상 클래스
class CompanyStrategy(ShippingStrategy):
    def calculate_additional_cost(self) -> float:
        pass

    @abstractmethod
    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        pass

    @abstractmethod
    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        pass

# 각 택배 회사 클래스들
class Hanjin(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 2500

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", f"{destination}에 {arrival_time}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=3, hours=3)

class PostOffice(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 2000

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["접수", f"{arrival_time} 도착 예정", f"{destination}에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=1, hours=2)

class CJ(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 3000

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["접수", "방금 출발", "지금 배송 중", "오늘 도착 예정", f"{destination} 에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=2, hours=5)

class Lotte(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 2500

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return ["배송 준비 완료", "배송 중", f"{destination} 에 도착"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=3, hours=12)

class DHL(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 40000

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time} 에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=5, hours=0)

class Amazon(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 40000

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time} 에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=7, hours=0)

class EMS(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 40000

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=5, hours=0)

class FedEx(CompanyStrategy):
    def calculate_cost(self, item_value: float, destination_country: str = "", item_weight: float = 0) -> float:
        return 40000

    def get_delivery_steps(self, destination: str, origin: str, departure_time: datetime) -> List[str]:
        arrival_time = self.calculate_arrival_time(departure_time)
        return [f"{origin}에서 {departure_time}에 출발", "배송 중", f"{destination}에 {arrival_time}에 도착", "배송 완료"]

    def calculate_arrival_time(self, departure_time: datetime) -> datetime:
        return departure_time + timedelta(days=7, hours=0)

# 배송 전략과 데코레이터, 택배사 팩토리
class ShippingFactory:
    strategies: Dict[str, Type[ShippingStrategy]] = {
        "일반": StandardShipping,
        "익일": NextDayShipping,
        "국제": InternationalShipping
    }

    decorators: Dict[str, Type[ShippingDecorator]] = {
        "보험": InsuranceDecorator,
    }

    companies: Dict[str, Type[CompanyStrategy]] = {
        "한진": Hanjin,
        "우체국": PostOffice,
        "CJ": CJ,
        "롯데": Lotte,
        "DHL": DHL,
        "Amazon": Amazon,
        "EMS": EMS,
        "FedEx": FedEx
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
        
        
# 옵저버 패턴 구현
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

# 옵저버 추상 클래스
class Observer(ABC):
    @abstractmethod
    def update(self, state: str) -> None:
        pass

# 지점 클래스(옵저버 구현)
class Branch(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, state: str) -> None:
        print(f"{self.name} 알림: {state}")

# 패키지 추적 클래스
class PackageTracker:
    def __init__(self, package_id: str):
        self.package_id = package_id
        self.history = []

    def update_status(self, status: str):
        self.history.append(status)
        print(f"패키지 {self.package_id} 상태 업데이트: {status}")

    def get_history(self) -> List[str]:
        return self.history

# 추적 가능한 패키지 클래스 (옵저버 패턴 구현)
class TrackedPackage(Subject):
    def __init__(self, package_id: str):
        super().__init__()
        self.tracker = PackageTracker(package_id)

    def set_state(self, state: str, event_type: str) -> None:
        self.tracker.update_status(state)
        self._state = state
        self.notify(event_type)

# 추적 가능한 패키지 설정 함수
def setup_tracked_package(destination: str, origin: str, shipping_type: str, package_id: str, decorator: Optional[str], company: Optional[str], item_value: float, destination_country: str, item_weight: float) -> None:
    package = TrackedPackage(package_id)
    branch_name = destination.capitalize() + " 지점"
    branch = Branch(branch_name)
    package.attach(branch, "배송 상태")

    # Use the current time as the departure time.
    departure_time = datetime.now()

    shipping_option = shipping_factory.get_shipping_strategy(shipping_type, decorator, company)
    arrival_time = shipping_option.calculate_arrival_time(departure_time)
    
    cost = shipping_option.calculate_cost(item_value, destination_country, item_weight)
    
    print(f"패키지 ID: {package_id}\n목적지: {destination}\n출발지: {origin}\n출발 시간: {departure_time}\n도착 예정 시간: {arrival_time}\n배송 유형: {shipping_type}\n데코레이터: {decorator}\n택배 회사: {company}\n비용: {cost} 원")

    steps = shipping_option.get_delivery_steps(destination, origin, departure_time)
    for step in steps:
        package.set_state(step, "배송 상태")
    package.detach(branch, "배송 상태")

    print(f"패키지 {package_id} 배송 기록:\n" + "\n".join(package.tracker.get_history()))

# 팩토리 인스턴스 생성
shipping_factory = ShippingFactory()

# 지역 선택 함수
def select_receive_location(is_international: bool) -> str:
    if is_international:
        country = input('목적지 국가를 선택하세요: ').strip()
        region = input(f'{country}의 지역을 선택하세요: ').strip()
        return f"{region}, {country}"
    else:
        return input('받는 사람의 지역을 입력하세요: ').strip()

def select_send_location(is_international: bool) -> str:
    if is_international:
        country = input('발송 국가를 선택하세요: ').strip()
        region = input(f'{country}의 지역을 선택하세요: ').strip()
        return f"{region}, {country}"
    else:
        return input('보내는 사람의 지역을 입력하세요: ').strip()

# 사용자 입력
print("어서오세요! \n택배는 사랑을 싣고 입니다! ")
is_international = input('해외 배송인가요? (예/아니오): ').strip().lower() == '예'
if is_international:
    shipping_type = "국제"
    company = input('해외 택배 회사를 선택하세요 (DHL/Amazon/EMS/FedEx): ').strip()
else:
    shipping_type = input('배송 방법을 입력하세요 (일반/익일): ').strip()
    company = input('택배 회사를 선택하세요 (한진/로젠/우체국/CJ/롯데): ').strip()
origin = select_send_location(is_international)
destination = select_receive_location(is_international)
item_weight = float(input('물품 무게를 입력하세요 (kg): ').strip())

decorator = input('보험을 선택하실 경우 입력하신 상품 가격의 10%가 추가 됩니다. (보험/없음): ').strip()
decorator = None if decorator == "없음" else decorator
item_value = float(input('상품 가격을 입력하세요 (원): ').strip())
destination_country = destination.split(",")[-1].strip()

# 패키지 ID 생성 및 설정
package_id = f"{destination}_{origin}_{shipping_type}_{company}_{hash(destination + origin + shipping_type + company)}"
setup_tracked_package(destination, origin, shipping_type, package_id, decorator, company, item_value, destination_country, item_weight)
