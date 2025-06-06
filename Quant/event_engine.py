import threading
import queue
from collections import defaultdict

class Event:
    """事件对象：封装事件类型和数据"""
    def __init__(self, type_, data=None):
        self.type_ = type_  # 事件类型（如 "tick", "order"）
        self.data = data    # 事件携带的数据

class EventBus:
    """事件总线：实现事件的订阅与发布"""
    def __init__(self):
        self._subscribers = defaultdict(list)  # {事件类型: [回调函数列表]}
        self._queue = queue.Queue()            # 事件队列（线程安全）
        self._active = False                   # 事件循环状态
        self._thread = None                    # 事件循环线程

    def subscribe(self, type_, handler):
        """订阅事件：注册回调函数"""
        self._subscribers[type_].append(handler)

    def publish(self, event):
        """发布事件：将事件放入队列"""
        self._queue.put(event)

    def _run(self):
        """事件循环：持续从队列取出事件并触发回调"""
        while self._active:
            try:
                event = self._queue.get(timeout=1)  # 1秒超时防止阻塞
                handlers = self._subscribers.get(event.type_, [])
                for handler in handlers:
                    handler(event)  # 调用回调函数
                self._queue.task_done()
            except queue.Empty:
                continue

    def start(self):
        """启动事件循环"""
        self._active = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """停止事件循环"""
        self._active = False
        self._thread.join()