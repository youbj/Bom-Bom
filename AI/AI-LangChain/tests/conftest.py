import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
root_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, root_dir)