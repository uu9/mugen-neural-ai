import ctypes
from ctypes import wintypes

# 定义需要的Windows API函数
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# FindWindow API
FindWindow = user32.FindWindowW
FindWindow.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindow.restype = wintypes.HWND

# GetWindowThreadProcessId API
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
GetWindowThreadProcessId.restype = wintypes.DWORD

# OpenProcess API
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

# ReadProcessMemory API
ReadProcessMemory = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    wintypes.HANDLE,
    wintypes.LPCVOID,
    ctypes.POINTER(ctypes.c_byte),
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t)
]
ReadProcessMemory.restype = wintypes.BOOL

# CloseHandle API
CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

# EnumWindows API
EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
EnumWindows.restype = wintypes.BOOL

# GetWindowText API
GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
GetWindowTextW.restype = ctypes.c_int

# GetClassName API
GetClassNameW = user32.GetClassNameW
GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
GetClassNameW.restype = ctypes.c_int

# GetLastError API
GetLastError = kernel32.GetLastError
GetLastError.restype = wintypes.DWORD

# VirtualQueryEx API - 用于检查内存区域信息
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

VirtualQueryEx = kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [
    wintypes.HANDLE,
    wintypes.LPCVOID,
    ctypes.POINTER(MEMORY_BASIC_INFORMATION),
    ctypes.c_size_t
]
VirtualQueryEx.restype = ctypes.c_size_t

# 常量定义
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x400

# 内存状态常量
MEM_COMMIT = 0x1000
# PAGE_READONLY | PAGE_READWRITE | PAGE_WRITECOPY
PAGE_READABLE = 0x02 | 0x04 | 0x40

# 内存读取错误代码
ERROR_MESSAGES = {
    0: "操作成功",
    6: "无效的句柄",
    299: "仅传输了部分数据",
    998: "无效的内存访问"
}

# 内存不可读原因
UNREADABLE_REASONS = {
    "HANDLE_EMPTY": "进程句柄为空",
    "VIRTUAL_QUERY_FAILED": "VirtualQueryEx调用失败",
    "NOT_COMMITTED": "内存区域未提交",
    "NOT_READABLE": "内存保护属性不允许读取",
    "OUT_OF_BOUNDS": "地址范围超出内存区域边界"
}

# 详细错误信息
DETAILED_ERROR_MESSAGES = {
    6: "进程句柄无效，可能进程已关闭",
    299: "只能读取部分数据，可能是内存保护或地址无效。这可能是因为偏移量不正确导致访问了无效内存地址，或者是目标进程内存布局发生了变化。",
    998: "无法访问指定内存地址，可能是地址无效或内存保护。请检查偏移量是否正确，以及目标内存地址是否有效。"
}