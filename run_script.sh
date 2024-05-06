#!/bin/bash

# KHS.py 실행
script_name="script/KHS.py"
# 이미 실행 중인지 확인 후, 실행 중이면 종료
pkill -f $script_name
# 스크립트 실행
python3 ~/ubuntu_shared_folder/GIT/CrawlingWeb/$script_name >> ~/ubuntu_shared_folder/GIT/CrawlingWeb/test.txt
