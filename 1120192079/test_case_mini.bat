@echo off
echo please ensure conda environment has been activated!
echo TESTING dev.py....... 
C:
cd C:\projects\downloader\1120192079
IF EXIST C:\projects\1744409-20220112155511412-749056801.png  del /q /s C:\projects\1744409-20220112155511412-749056801.png


echo #############test_case 1 pic#################
python dev.py -u https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png -o ../../

pause