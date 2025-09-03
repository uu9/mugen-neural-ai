import os
from loguru import logger
import numpy as np

from models import FrameStatus
from mugen_memory_reader import MugenMemoryHelper


class DataProcessor:
    def __init__(self, save_seq: int | None = None):
        self.data_dir = "data"
        self.save_seq = save_seq or self.get_save_seq()
        self.save_name = f"{self.save_seq}.npy"
        self.data = np.zeros(shape=(0, 19), dtype=float)

    def add_status(self, status: FrameStatus):
        self.data = np.append(
            self.data,
            np.array(
                [
                    [
                        status.current_frames,
                        status.player_1_status.player_life,
                        status.player_1_status.player_power,
                        status.player_1_status.player_move_type,
                        status.player_1_status.player_state_no,
                        status.player_1_status.player_prev_state_no,
                        status.player_1_status.player_pos_x,
                        status.player_1_status.player_pos_y,
                        status.player_1_status.player_vel_x,
                        status.player_1_status.player_vel_y,
                        status.player_2_status.player_life,
                        status.player_2_status.player_power,
                        status.player_2_status.player_move_type,
                        status.player_2_status.player_state_no,
                        status.player_2_status.player_prev_state_no,
                        status.player_2_status.player_pos_x,
                        status.player_2_status.player_pos_y,
                        status.player_2_status.player_vel_x,
                        status.player_2_status.player_vel_y,
                    ]
                ]
            ), axis=0)

    def get_save_seq(self):
        data_list = os.listdir(self.data_dir)
        data_list = sorted(data_list)
        if len(data_list) > 0:
            last_file = data_list[-1]
            last_file_num = int(last_file.split(".")[0])
            return last_file_num + 1
        else:
            return 0

    def save(self):
        np.save(os.path.join(self.data_dir, self.save_name), self.data)
        return self.save_seq


def main():
    with MugenMemoryHelper() as helper:
        logger.info(
            f"""窗口句柄: {helper.pm.process_handle}\n进程ID: {helper.pm.process_id}\n基址: 0x{helper.pm.base_address:X}""")
        helper.pause(True)

        data_processor = DataProcessor()
        while True:
            current_frames = after_step_frames = helper.read_frames()
            logger.info(f"游戏帧数：{current_frames}")
            while after_step_frames != current_frames + 1:
                if after_step_frames > current_frames + 1:
                    logger.warning("帧数被跳过")
                if after_step_frames != current_frames:
                    logger.debug(
                        f"上一帧：{current_frames}, 差值：{after_step_frames - current_frames}")
                # round 结束
                if after_step_frames < current_frames:
                    current_frames = after_step_frames
                    save_seq = data_processor.save()
                    data_processor = DataProcessor(save_seq=save_seq+1)
                data_processor.add_status(helper.read_status())
                helper.step_frame()
                after_step_frames = helper.read_frames()


if __name__ == "__main__":
    main()
