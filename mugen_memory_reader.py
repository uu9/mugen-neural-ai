import ctypes
from time import sleep
import pymem
import pymem.exception
import pymem.process
from pymem import Pymem

from models import FrameStatus, PlayerStatus
from mugen_database import Mugen11B1DB

from utils.log import logger

class MugenMemoryHelper:
    def __init__(self):
        if not self.is_admin():
            raise PermissionError("Please run this program with administrator privileges")
        self.title = "M.U.G.E.N"
        self.class_name = "SDL_app"
        self.executable_name = "mugen.exe"
        # pymem instance
        self.pm = Pymem(self.executable_name)
        self.db = Mugen11B1DB()

        self.base_addr = self._get_base_addr()


    def open_process(self):
        pass

    def close_process(self):
        """
        Close process handle
        """
        self.pm.close_process()
        self.pm = None

    def _get_base_addr(self):
        base_addr = self.pm.read_int(self.db.MUGEN_POINTER_BASE_OFFSET)
        # logger.debug(f"Base Addr: {base_addr}")
        return base_addr

    def _get_player_base(self, player_num):
        """
        Get player base address
        """
        addr = self.base_addr + self.db.PLAYER_1_BASE_OFFSET + 4 * (player_num - 1)
        player_base = self.pm.read_int(addr)
        # logger.debug(f"Player {player_num} Base: {player_base}")
        return player_base

    def read_player_life(self, player_num):
        """
        Read player life value
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.LIFE_PLAYER_OFFSET)
    
    def read_player_pos_x(self, player_num):
        """
        Read player X-axis coordinate
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.POS_X_PLAYER_OFFSET)
    
    def read_player_pos_y(self, player_num):
        """
        Read player Y-axis coordinate
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.POS_Y_PLAYER_OFFSET)
    
    def read_player_vel_x(self, player_num):
        """
        Read player X-axis velocity
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.VEL_X_PLAYER_OFFSET)
    
    def read_player_vel_y(self, player_num):
        """
        Read player Y-axis velocity
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_double(player_base + self.db.VEL_Y_PLAYER_OFFSET)
    
    def read_player_state_no(self, player_num):
        """
        Read player state number
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.STATE_NO_PLAYER_OFFSET)
    
    def read_player_prev_state_no(self, player_num):
        """
        Read player previous frame state number
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.PREV_STATE_NO_PLAYER_OFFSET)
    
    def read_player_power(self, player_num):
        """
        Read player power
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.POWER_PLAYER_OFFSET)
    
    def read_player_move_type(self, player_num):
        """
        Read player move type
        """
        player_base = self._get_player_base(player_num)
        return self.pm.read_int(player_base + self.db.MOVE_TYPE_PLAYER_OFFSET)
    
    def read_frames(self):
        """
        Read game frames
        """
        game_base = self.read_base_address()
        return self.pm.read_int(game_base + self.db.ROUND_TIME_BASE_OFFSET)
    
    def step_frame(self):
        """
        Simulate a game frame
        """
        self.inject_command(46)
        

    def pause(self, is_paused):
        """
        Pause the game
        """
        pause_state = 1 if is_paused else 0
        game_base = self.read_base_address()
        self.pm.write_int(game_base + self.db.PAUSE_ADDR, pause_state)
    
    def read_base_address(self):
        """
        Read the base address of the Mugen game process
        """
        return self.pm.read_int(self.db.MUGEN_POINTER_BASE_OFFSET)
    
    def inject_command(self, command: int):
        """
        Inject command
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
        Check if the current program is running with administrator privileges
        """
        return ctypes.windll.shell32.IsUserAnAdmin()
    
    def read_status(self):
        player_num=1
        player_1_status = PlayerStatus(
            player_num=player_num,
            player_life=self.read_player_life(player_num),
            player_power=self.read_player_power(player_num),
            player_move_type=self.read_player_move_type(player_num),
            player_state_no=self.read_player_state_no(player_num),
            player_prev_state_no=self.read_player_prev_state_no(player_num),
            player_pos_x=self.read_player_pos_x(player_num),
            player_pos_y=self.read_player_pos_y(player_num),
            player_vel_x=self.read_player_vel_x(player_num),
            player_vel_y=self.read_player_vel_y(player_num),
        )
        player_num=2
        player_2_status = PlayerStatus(
            player_num=player_num,
            player_life=self.read_player_life(player_num),
            player_power=self.read_player_power(player_num),
            player_move_type=self.read_player_move_type(player_num),
            player_state_no=self.read_player_state_no(player_num),
            player_prev_state_no=self.read_player_prev_state_no(player_num),
            player_pos_x=self.read_player_pos_x(player_num),
            player_pos_y=self.read_player_pos_y(player_num),
            player_vel_x=self.read_player_vel_x(player_num),
            player_vel_y=self.read_player_vel_y(player_num),
        )

        return FrameStatus(
            current_frames=self.read_frames(),
            player_1_status=player_1_status,
            player_2_status=player_2_status,
        )



if __name__ == "__main__":
    with MugenMemoryHelper() as helper:
        logger.info(f"""Window Handle: {helper.pm.process_handle}\nProcess ID: {helper.pm.process_id}\nBase Address: 0x{helper.pm.base_address:X}""")
        helper.pause(True)

        while True:
            # logger.info(f"Player 1 Life: {helper.read_player_life(1)}")
            # logger.info(f"Player 2 Life: {helper.read_player_life(2)}")
            # logger.info(f"Player 1 Position: ({helper.read_player_pos_x(1)}, {helper.read_player_pos_y(1)})")
            # logger.info(f"Player 2 Position: ({helper.read_player_pos_x(2)}, {helper.read_player_pos_y(2)})")
            # logger.info(f"Player 1 Velocity: ({helper.read_player_vel_x(1)}, {helper.read_player_vel_y(1)})")
            # logger.info(f"Player 2 Velocity: ({helper.read_player_vel_x(2)}, {helper.read_player_vel_y(2)})")
            # logger.info(f"Player 1 State Number: {helper.read_player_state_no(1)}")
            # logger.info(f"Player 2 State Number: {helper.read_player_state_no(2)}")
            # logger.info(f"Player 1 Previous State Number: {helper.read_player_prev_state_no(1)}")
            # logger.info(f"Player 2 Previous State Number: {helper.read_player_prev_state_no(2)}")
            # logger.info(f"Player 1 Power: {helper.read_player_power(1)}")
            # logger.info(f"Player 2 Power: {helper.read_player_power(2)}")
            # logger.info(f"Player 1 Move Type: {helper.read_player_move_type(1)}")
            # logger.info(f"Player 2 Move Type: {helper.read_player_move_type(2)}")
            current_frames  = after_step_frames = helper.read_frames()
            logger.info(f"Game Frame: {current_frames}")
            while after_step_frames != current_frames + 1:
                if after_step_frames > current_frames + 1:
                    logger.warning("Frame skipped")
                if after_step_frames != current_frames:
                    logger.debug(f"Previous frame: {current_frames}, Difference: {after_step_frames - current_frames}")
                # Round ended
                if after_step_frames < current_frames:
                    current_frames = after_step_frames
                helper.step_frame()
                after_step_frames = helper.read_frames()