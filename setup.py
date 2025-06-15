import os
import sys
os.system(f'"{sys.executable}" -m pip install -q -r requirements.txt')
os.system(f'"{sys.executable}"  playwright install')
print("You can now run the application with: python main.py")