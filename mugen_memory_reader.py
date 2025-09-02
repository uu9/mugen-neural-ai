import ctypes
from time import sleep
import pymem
import pymem.exception
import pymem.process
from pymem import Pymem

from mugen_database import Mugen11B1DB

from utils.log import logger

class MugenMemoryHelper:
    def __init__(self):
        if not self.is_admin():
            raise PermissionError("请以管理员权限运行本程序")
        self.title = "M.U.G.E.N"
        self.class_name = "SDL_app"
        self.executable_name = "mugen.exe"
        # pymem实例
        self.pm = Pymem(self.executable_name)
        self.db = Mugen11B1DB()

        self.base_addr = self._get_base_addr()


    def open_process(self):
        pass

    def close_process(self):
        """
        关闭进程句柄
        """
        self.pm.close_process()
        self.pm = None

    def _get_base_addr(self):
        base_addr = self.pm.read_int(self.db.MUGEN_POINTER_BASE_OFFSET)
        logger.debug(f"Base Addr: {base_addr}")
        return base_addr

    def _get_player_base(self, player_num):
        """
        获取玩家基地址
        """
        addr = self.base_addr + self.db.PLAYER_1_BASE_OFFSET + 4 * (player_num - 1)
        player_base = self.pm.read_int(addr)
        logger.debug(f"Player {player_num} Base: {player_base}")
        return player_base

    def read_player_life(self, player_num):
        """
        读取玩家生命值
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.LIFE_PLAYER_OFFSET)
    
    def read_player_pos_x(self, player_num):
        """
        读取玩家X轴坐标
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.POS_X_PLAYER_OFFSET)
    
    def read_player_pos_y(self, player_num):
        """
        读取玩家Y轴坐标
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.POS_Y_PLAYER_OFFSET)
    
    def read_player_vel_x(self, player_num):
        """
        读取玩家X轴速度
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.VEL_X_PLAYER_OFFSET)
    
    def read_player_vel_y(self, player_num):
        """
        读取玩家Y轴速度
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.VEL_Y_PLAYER_OFFSET)
    
    def read_player_state_no(self, player_num):
        """
        读取玩家状态编号
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.STATE_NO_PLAYER_OFFSET)
    
    def read_player_prev_state_no(self, player_num):
        """
        读取玩家上一帧状态编号
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.PREV_STATE_NO_PLAYER_OFFSET)
    
    def read_player_power(self, player_num):
        """
        读取玩家能量
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.POWER_PLAYER_OFFSET)
    
    def read_player_move_type(self, player_num):
        """
        读取玩家移动类型
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.MOVE_TYPE_PLAYER_OFFSET)
    
    def read_frames(self):
        """
        读取游戏帧数
        """
        game_base = self.read_base_address()
        return self.pm.read_int(game_base + self.db.ROUND_TIME_BASE_OFFSET)
    
    def step_frame(self):
        """
        模拟一个游戏帧
        """
        self.inject_command(46)
        

    def pause(self, is_paused):
        """
        暂停游戏
        """
        pause_state = 1 if is_paused else 0
        game_base = self.read_base_address()
        self.pm.write_int(game_base + self.db.PAUSE_ADDR, pause_state)
    
    def read_base_address(self):
        """
        读取Mugen游戏进程的基址
        """
        return self.pm.read_int(self.db.MUGEN_POINTER_BASE_OFFSET)
    
    def inject_command(self, command: int):
        """
        注入命令
        """
        self.pm.write_int(self.db.CMD_KEY_ADDR, command | 256)
        self.pm.write_int(self.db.CMD_KEY_ADDR + 4, command | 768)
        self.pm.write_int(self.db.CMD_NEXT_INDEX_ADDR, 1)
        self.pm.write_int(self.db.CMD_CURRENT_INDEX_ADDR, 0)

    def __enter__(self):
        self.open_process()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_process()

    def is_admin(self):
        """
        检查当前是否以管理员权限运行
        """
        return ctypes.windll.shell32.IsUserAnAdmin()


if __name__ == "__main__":
    with MugenMemoryHelper() as helper:
        logger.info(f"""窗口句柄: {helper.pm.process_handle}\n进程ID: {helper.pm.process_id}\n基址: 0x{helper.pm.base_address:X}""")
        helper.pause(True)

        while True:
            # logger.info(f"玩家 1 生命值：{helper.read_player_life(1)}")
            # logger.info(f"玩家 2 生命值：{helper.read_player_life(2)}")
            # logger.info(f"玩家 1 坐标：({helper.read_player_pos_x(1)}, {helper.read_player_pos_y(1)})")
            # logger.info(f"玩家 2 坐标：({helper.read_player_pos_x(2)}, {helper.read_player_pos_y(2)})")
            # logger.info(f"玩家 1 速度：({helper.read_player_vel_x(1)}, {helper.read_player_vel_y(1)})")
            # logger.info(f"玩家 2 速度：({helper.read_player_vel_x(2)}, {helper.read_player_vel_y(2)})")
            # logger.info(f"玩家 1 状态编号：{helper.read_player_state_no(1)}")
            # logger.info(f"玩家 2 状态编号：{helper.read_player_state_no(2)}")
            # logger.info(f"玩家 1 上一帧状态编号：{helper.read_player_prev_state_no(1)}")
            # logger.info(f"玩家 2 上一帧状态编号：{helper.read_player_prev_state_no(2)}")
            # logger.info(f"玩家 1 能量：{helper.read_player_power(1)}")
            # logger.info(f"玩家 2 能量：{helper.read_player_power(2)}")
            # logger.info(f"玩家 1 移动类型：{helper.read_player_move_type(1)}")
            # logger.info(f"玩家 2 移动类型：{helper.read_player_move_type(2)}")
            current_frames  = after_step_frames = helper.read_frames()
            logger.info(f"游戏帧数：{current_frames}")
            while after_step_frames != current_frames + 1:
                if after_step_frames > current_frames + 1:
                    raise Exception("帧数被跳过")
                if after_step_frames != current_frames:
                    logger.debug(f"上一帧：{current_frames}, 差值：{after_step_frames - current_frames}")
                # round 结束
                if after_step_frames < current_frames:
                    current_frames = after_step_frames
                helper.step_frame()
                after_step_frames = helper.read_frames()
