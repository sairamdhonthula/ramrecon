@echo off
git add . > git_log.txt 2>&1
git commit -m "push code" >> git_log.txt 2>&1
git remote add origin https://github.com/sairamdhonthula/ramrecon.git >> git_log.txt 2>&1
git push -u origin main >> git_log.txt 2>&1
git push -u origin master >> git_log.txt 2>&1
echo DONE >> git_log.txt
exit
