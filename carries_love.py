from abc import ABC, abstractmethod
from threading import Lock

# 싱글턴 패턴: 데이터베이스 관리
class DatabaseManager:
    _instance = None
    _lock = Lock()

    # 싱글턴 구현: 인스턴스 생성 제어,
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._data = {}  # 가상의 데이터베이스
        return cls._instance

    # 데이터 읽기
    def get_data(self, key):
        return self._data.get(key)

    # 데이터 쓰기
    def set_data(self, key, value):
        self._data[key] = value

# 팩토리 메소드 패턴: 배송 전략
class ShippingStrategy(ABC):

    # 비용 계산 추상 메소드
    @abstractmethod
    def calculate_cost(self):
        pass

# 표준 배송 클래스
class StandardShipping(ShippingStrategy):
    def calculate_cost(self):
        return 5.00

# 익일 배송 클래스
class NextDayShipping(ShippingStrategy):
    def calculate_cost(self):
        return 20.00

# 국제 배송 클래스
class InternationalShipping(ShippingStrategy):
    def calculate_cost(self):
        return 15.00

# 배송 전략 팩토리
class ShippingFactory:
    def get_shipping_strategy(self, type):
        if type == "standard":
            return StandardShipping()
        elif type == "nextday":
            return NextDayShipping()
        elif type == "international":
            return InternationalShipping()
        else:
            raise ValueError("Unknown shipping type")

# 옵저버 패턴: 상태 변화 관찰 및 통지
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None

    # 옵저버 등록
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    # 옵저버 제거
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    # 옵저버에게 상태 변화 통지
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    # 상태 설정 및 통지
    def set_state(self, state):
        self._state = state
        self.notify()

# 옵저버 추상 클래스
class Observer(ABC):
    def update(self, state):
        pass

# 지점 클래스 (옵저버 구현)
class Branch(Observer):
    def __init__(self, name):
        self.name = name

    # 상태 업데이트 시 수행 작업
    def update(self, state):
        print(f"{self.name} branch notified of package state: {state}")

# 예제 사용
db = DatabaseManager()
shipping_factory = ShippingFactory()
package = Subject()

# 도착지에 따라 동적으로 지점 생성 및 등록
destination = "Yongin"
if destination == "Yongin":
    Yongin_branch = Branch("Yongin")
    package.attach(Yongin_branch)

shipping_option = shipping_factory.get_shipping_strategy("standard")
print(f"Shipping cost: {shipping_option.calculate_cost()} 원")

package.set_state("Arrived in Yongin")
