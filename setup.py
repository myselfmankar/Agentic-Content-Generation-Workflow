import os
import sys
os.system(f'"{sys.executable}" -m pip install -r requirements.txt')
os.system(f'"{sys.executable}" -m playwright install')
print("You can now run the application with: python main.py")