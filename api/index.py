from os import path
import sys

ROOT_DIR = path.dirname(path.dirname(__file__)) # repo root (api/..)
SRC_DIR = path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
	sys.path.insert(0, SRC_DIR)

from fiap_tech_cha_fase1.app.main import app

