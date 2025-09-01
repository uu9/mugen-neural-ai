import pymem
import pymem.process
import ctypes

# Mugen不同版本的HP偏移量
MUGEN_VERSION_OFFSETS = {
    'mugen11': 0x1B8,  # 根据分析结果，Mugen 1.1中HP偏移量为0x1B8
    'mugen10': 0x1BC,  # 根据分析结果，Mugen 1.0中HP偏移量为0x1BC
    'winmugen': 0x160  # 根据分析结果，WinMugen中HP偏移量为0x160
}

# 玩家基址 - 这些值需要根据实际游戏版本进行调整
PLAYER_1_BASE_ADDRESS = 0x00980080  # 示例值，实际需要根据游戏版本确定
PLAYER_2_BASE_ADDRESS = 0x00980084  # 示例值，实际需要根据游戏版本确定

def read_mugen_hp(process_name="mugen.exe", version='mugen11'):
    """
    读取Mugen游戏中人物的HP值
    
    Args:
        process_name: 进程名称，默认为"mugen.exe"
        version: Mugen版本，默认为'mugen11'
    
    Returns:
        tuple: (player1_hp, player2_hp)
    """
    try:
        # 连接到进程
        pm = pymem.Pymem(process_name)
        
        # 获取偏移量
        hp_offset = MUGEN_VERSION_OFFSETS.get(version, MUGEN_VERSION_OFFSETS['mugen11'])
        
        # 读取玩家1的HP
        # 首先读取玩家1的基址
        player1_base = pm.read_int(PLAYER_1_BASE_ADDRESS)
        # 然后从基址加上偏移量读取HP值
        player1_hp = pm.read_int(player1_base + hp_offset)
        
        # 读取玩家2的HP
        # 首先读取玩家2的基址
        player2_base = pm.read_int(PLAYER_2_BASE_ADDRESS)
        # 然后从基址加上偏移量读取HP值
        player2_hp = pm.read_int(player2_base + hp_offset)
        
        return (player1_hp, player2_hp)
    
    except pymem.exception.ProcessNotFound:
        print(f"未找到进程: {process_name}")
        return None
    except pymem.exception.CouldNotOpenProcess:
        print(f"无法打开进程: {process_name}，请确保以管理员权限运行")
        return None
    except Exception as e:
        print(f"读取HP时发生错误: {str(e)}")
        return None

def main():
    print("Mugen HP读取器")
    print("确保Mugen游戏正在运行...")
    
    # 读取HP值
    hp_values = read_mugen_hp()
    
    if hp_values:
        player1_hp, player2_hp = hp_values
        print(f"玩家1 HP: {player1_hp}")
        print(f"玩家2 HP: {player2_hp}")
    else:
        print("无法读取HP值")

if __name__ == "__main__":
    main()