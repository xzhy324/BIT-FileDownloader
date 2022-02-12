@echo please ensure conda environment has been activated!
@echo TESTING dev.py....... 
@C:
@cd C:\projects\downloader\1120192079

@echo test_case 1
python downloader.py -u https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png

@echo test_case 2
python downloader.py -u https://dldir1.qq.com/weixin/Windows/WeChatSetup.exe -o ../../

@echo test_case 3
python downloader.py -u https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz -o ../../



pause