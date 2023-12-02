import tyro

from frame_transformer.systems import System
from frame_transformer.frame_transformer import FrameTransformer

def main(origin: System, target: System):
    """
        This function is the entrypoint of the program.
        Args:
            origin: The origin system.
            target: The target system.
    """
    transformer = FrameTransformer(origin, target)
    transformer.explain()

def entrypoint():
    tyro.cli(main)

if __name__ == "__main__":
    entrypoint()