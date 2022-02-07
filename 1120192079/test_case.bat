@echo please ensure conda environment has been activated!
@echo TESTING dev.py....... 
@C:
@cd C:\projects\downloader\1120192079

@echo test_case 1
python dev.py -u https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png

@echo test_case 2
python dev.py -u https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz -o ../../

@echo test_case 3
python dev.py -u https://opus.nlpl.eu/download.php?f=ada83/v1/tmx/en-ru.tmx.gz -o ../../

pause