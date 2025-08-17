# PyQt5 线程入门示例：QObject + QThread（推荐模式）  # 模块说明
# 目的：演示如何在 PyQt5 中用一个工作对象（QObject）和一个后台线程（QThread）来执行耗时任务，
#       同时通过信号与槽把结果回传给 UI，确保 UI 不会因为在子线程操作而崩溃。
# 注释要点：
# - UI 线程只负责界面展示，所有耗时工作放在子线程执行，确保界面始终响应
# - 使用信号（pyqtSignal）向主线程汇报进度、日志、错误等，避免直接操作 UI
# - 在线程结束时做统一清理，避免“Destroyed while thread is still running”的崩溃
# - 提供“开始/暂停/重来”等交互，确保在记满或暂停后 UI 仍可继续使用
# 运行前：
#     pip install PyQt5
# 运行：
#     python PythonStudy/Thread.py
# -------------------- 代码开始 --------------------
import sys  # 系统级别的入口/退出和命令行参数处理
import time  # 用于模拟耗时操作的时间睡眠
import traceback  # 捕获异常信息并打印，辅助调试
from typing import Optional  # 表示变量可能为 None 的类型提示

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot  # PyQt 的核心对象、线程与信号相关
from PyQt5.QtWidgets import (  # UI 小部件集合
    QApplication,  # 应用对象，管理事件循环
    QWidget,  # 作为主窗口的基本容器
    QVBoxLayout,  # 垂直布局管理器，方便控件竖向排序
    QPushButton,  # 按钮控件，用户交互
    QProgressBar,  # 进度条控件，显示进度
    QTextEdit,  # 多行文本编辑控件，日志输出用
    QLabel,  # 标签控件，用于静态文本显示
    QMessageBox,  # 弹窗对话框，用于错误提示
)


#这个地方ok
# 全局异常钩子，用于防止未捕获异常导致应用直接崩溃 
def install_excepthook() -> None:
    def _handle(exctype, value, tb):
        # 将未捕获异常的完整信息输出到控制台，方便定位
        traceback.print_exception(exctype, value, tb)  #异常类型、异常值、追踪对象
        try:
            # 同时在 GUI 中弹窗告知用户异常信息
            QMessageBox.critical(None, "未捕获异常", f"{exctype.__name__}: {value}")
        except Exception:
            # 如果弹窗失败，确保不再抛出异常
            pass #空操作，什么都不做
    # 将全局异常处理函数设置为系统默认行为
    sys.excepthook = _handle


class BackgroundWorker(QObject):  # 定义后台工作者类，继承自 QObject
    """在子线程中运行的工作者。
    
    通过特定的信号把信息传回主线程，以更新 UI。
    """

    # 信号：表示当前进度百分比，范围 [0, 100]
    progress_changed = pyqtSignal(int)
    # 信号：携带文本的日志信息或普通消息
    message_emitted = pyqtSignal(str)
    # 信号：工作完成，通知主线程可以清理或接续下一步
    finished = pyqtSignal()
    # 信号：发生错误，携带错误信息文本
    error_occurred = pyqtSignal(str)

    def __init__(self, total_steps: int = 100, start_step: int = 0, delay_seconds: float = 0.03) -> None:
        super().__init__()
        self._total_steps = total_steps
        self._start_step = int(max(0, start_step))  # 起始步，从 0 开始计数
        self._delay_seconds = delay_seconds  # 每步的耗时，模拟实际工作
        self._should_stop = False  # 控制是否应停止执行，便于协作式取消

    @pyqtSlot()
    def run(self) -> None:
        """在子线程中执行耗时任务；通过信号与 UI 线程通信。"""
        try:
            self.message_emitted.emit("任务开始")  # 通知 UI 任务已开始
            # 从起始步开始计数，确保可以从当前进度继续执行
            for step_index in range(self._start_step + 1, self._total_steps + 1): #从start_step+1开始，到total_steps+1结束
                if self._should_stop:  # 遇到停止请求，执行清理工作并跳出循环
                    self.message_emitted.emit("收到停止请求，正在清理…")
                    break
                time.sleep(self._delay_seconds)  # 模拟耗时操作
                progress_percent = int(step_index / self._total_steps * 100)  # 计算当前进度百分比
                self.progress_changed.emit(progress_percent)  # 将进度结果发送回 UI
                if step_index % 10 == 0:  # 每完成 10% 记录一次日志，有助于观测进度
                    self.message_emitted.emit(f"已完成 {progress_percent}%")
            else:
                self.message_emitted.emit("任务正常完成")  # 循环正常结束时的日志
        except Exception as exc:  # 捕获任何未预料的异常，防止子线程崩溃
            self.error_occurred.emit(f"子线程异常: {exc!r}")
        finally:
            self.finished.emit()  # 无论如何，任务结束后发送完成信号

    @pyqtSlot()
    def stop(self) -> None:
        """请求停止任务（协作式取消），通过设置标志位实现自愿退出。"""
        self._should_stop = True  # 设置停止标志，下一轮循环会检测到并退出

class MainWindow(QWidget):  # 主窗口类，负责 UI 与线程协调
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQt5 线程入门示例：QObject + QThread")  # 设置窗口标题，方便识别
        #使用 Optional 1. 明确表示变量可能为 None2. 提供类型安全3. 帮助 IDE 和类型检查器进行静态类型检查
        self._thread: Optional[QThread] = None  # 保存后台线程引用，便于后续控制
        self._worker: Optional[BackgroundWorker] = None  # 保存工作者对象引用，便于发送控制指令
        self._total_steps = 120  # 总步数，决定任务的工作量
        self._is_running = False  # 表示当前是否有任务在运行，避免重复启动
        self._build_ui()  # 构建界面布局与控件

    def _build_ui(self) -> None:
        # 创建交互控件
        self._start_button = QPushButton("开始任务")  # 点击启动后台任务
        self._stop_button = QPushButton("暂停/停止任务")  # 点击停止当前任务
        self._stop_button.setEnabled(False)  # 初始状态下不可点击停止

        self._reset_button = QPushButton("重来")  # 新增：重置进度，重新从 0 开始
        self._reset_button.setEnabled(False)  # 初始时不可用，只有有进度时才可用

        self._status_label = QLabel("就绪")  # 显示当前状态的文本标签
        #QProgressBar 进度条控件，用于显示任务进度
        self._progress_bar = QProgressBar()  # 用于显示任务进度的控件
        self._progress_bar.setRange(0, 100)  # 进度条的取值范围
        self._progress_bar.setValue(0)  # 初始进度为 0

        self._log_text = QTextEdit()  # 日志输出区域
        self._log_text.setReadOnly(True)  # 日志区域设为只读，防止修改

        layout = QVBoxLayout()  # 垂直布局容器，将控件竖向摆放
        layout.addWidget(self._status_label)  # 状态文本
        layout.addWidget(self._progress_bar)  # 进度条
        layout.addWidget(self._start_button)  # 开始按钮
        layout.addWidget(self._stop_button)  # 暂停/停止按钮
        layout.addWidget(self._reset_button)  # 重来按钮
        layout.addWidget(QLabel("日志："))  # 日志标题
        layout.addWidget(self._log_text)  # 日志文本区域
        self.setLayout(layout)  # 应用布局到主窗口

        # 绑定事件：点击按钮时触发对应的方法
        self._start_button.clicked.connect(self._on_start_clicked)
        self._stop_button.clicked.connect(self._on_stop_clicked)
        self._reset_button.clicked.connect(self._on_reset_clicked)

    @pyqtSlot()
    def _on_start_clicked(self) -> None:
        # 进入开始逻辑前，先检查是否已有任务在运行，避免并发启动
        if self._is_running:
            return  # 直接返回，不重复启动

        current_progress = self._progress_bar.value()  # 读取当前进度，用于决定起点
        if current_progress >= 100:  # 如果已经记满，必须通过重来重新开始
            self._log_text.append("[提示] 已完成，请点击“重来”以从0重新开始")
            return

        # 计算从当前进度对应的起始步，确保“从当前进度继续”行为正确
        start_step = int(current_progress / 100 * self._total_steps)

        self._status_label.setText("运行中…")  # 更新状态提示
        self._start_button.setEnabled(False)  # 禁用开始，防止再次点击造成冲突
        self._stop_button.setEnabled(True)  # 允许用户暂停/停止任务
        self._progress_bar.setValue(current_progress)  # 保留当前进度，不重置为 0
        self._log_text.clear()  # 清理日志区域，给新任务一个干净的日志区

        # 创建工作者与线程，并把工作者移动到线程中执行
        self._worker = BackgroundWorker(total_steps=self._total_steps, start_step=start_step, delay_seconds=0.02)
        self._thread = QThread() #创建一个线程对象
        self._worker.moveToThread(self._thread) #将工作者对象移动到线程中执行
        self._thread.started.connect(self._worker.run) #当线程启动时，调用工作者对象的run方法

        # 连接信号与 UI 槽，实时更新界面
        self._thread.finished.connect(self._on_thread_finished)  # 在线程结束时调用统一清理

        self._worker.progress_changed.connect(self._on_progress_changed) 
        self._worker.message_emitted.connect(self._on_message_emitted)
        self._worker.error_occurred.connect(self._on_error_occurred)
        self._worker.finished.connect(self._on_worker_finished)

        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._worker.finished.connect(self._worker.deleteLater)

        self._thread.start()
        self._is_running = True  # 标记当前有任务在运行，防止重复启动
        self._reset_button.setEnabled(current_progress > 0)  # 仅当有进度时允许重来（从此继续）

    @pyqtSlot()
    def _on_stop_clicked(self) -> None:
        # 暂停/停止任务，触发协作式取消
        if self._worker is not None:
            self._worker.stop()
            self._status_label.setText("暂停中…")
            self._stop_button.setEnabled(False)
            self._is_running = False  # 运行标记改为 False，允许后续重新开始

    @pyqtSlot(int) # _on_progress_changed 不会"自动"执行，而是在信号 emit() 时被触发。
    def _on_progress_changed(self, percent: int) -> None:
        self._progress_bar.setValue(percent)  # 更新进度条显示的百分比
        if percent > 0:
            self._reset_button.setEnabled(True)  # 有进度时允许“重来”

    @pyqtSlot(str)
    def _on_message_emitted(self, message: str) -> None:
        self._log_text.append(message)  # 将日志消息追加到文本区

    @pyqtSlot(str)
    def _on_error_occurred(self, message: str) -> None:
        self._log_text.append(f"[错误] {message}")  # 以错误前缀输出错误信息

    @pyqtSlot()
    def _on_worker_finished(self) -> None:
        # 工作线程报告完成，但我们不在这里直接销毁线程对象
        self._is_running = False  # 更新运行状态为非运行
        self._stop_button.setEnabled(False)  # 禁用停止按钮
        self._start_button.setEnabled(True)  # 重新启用开始按钮

        if self._progress_bar.value() < 100:
            self._reset_button.setEnabled(True if self._progress_bar.value() > 0 else False)
        else:
            self._reset_button.setEnabled(True)  # 已完成，允许通过重来从0重新开始

    @pyqtSlot()
    def _on_thread_finished(self) -> None:
        # 线程真正结束后统一清理引用，确保不会在子线程仍在运行时销毁对象
        self._thread = None
        self._worker = None
        self._is_running = False
        self._status_label.setText("已结束")
        self._start_button.setEnabled(True)
        self._stop_button.setEnabled(False)

        # 保留当前进度，但允许通过重来重新开始
        if self._progress_bar.value() < 100:
            self._reset_button.setEnabled(True if self._progress_bar.value() > 0 else False)
        else:
            self._reset_button.setEnabled(True)

    @pyqtSlot()
    def _on_reset_clicked(self) -> None:
        # 重置进度到 0，停止状态，允许重新开始
        if self._thread is not None:
            return  # 运行中时不允许重置
        self._progress_bar.setValue(0)
        self._status_label.setText("就绪")
        self._start_button.setEnabled(True)
        self._stop_button.setEnabled(False)
        self._reset_button.setEnabled(False)
        self._log_text.append("进度已重置为 0")

    def closeEvent(self, event):  # 窗口关闭时的保护性处理
        if self._thread is not None and self._thread.isRunning():  # 若有线程在运行
            if self._worker is not None:
                self._worker.stop()  # 通过协作式取消停止工作
            self._thread.quit()  # 请求线程退出
            self._thread.wait(3000)  # 最多等待 3 秒让线程收尾
        event.accept()  # 允许关闭窗口

def main() -> None:
    app = QApplication(sys.argv)  # 创建应用对象
    install_excepthook()  # 安装全局未捕获异常处理，避免崩溃退出
    window = MainWindow()  # 创建主窗口
    window.resize(520, 420)  # 设置初始窗口尺寸
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入事件循环

if __name__ == "__main__":  # 脚本直接执行时运行
    main()  # 启动应用