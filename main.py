from datetime import datetime
import torch
import torch_directml
from utils.log import logger

DEVICE = torch_directml.device()
logger.info(f"DirectML Info: {DEVICE}")


def main():
    time_start = datetime.now()
    size = 10000
    tensor1 = torch.rand(size, size, device=DEVICE)
    tensor2 = torch.rand(size, size, device=DEVICE)
    dml_algebra = tensor1 * tensor2
    time_end = datetime.now()
    time_elapsed = time_end - time_start
    print("time cost:")
    print(time_elapsed.seconds)


if __name__ == "__main__":
    main()