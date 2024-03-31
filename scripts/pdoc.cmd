echo on
if exist .\public rmdir .\public /s /q
set PYTHONPATH=.
@REM cd ../
set PDOC=true
call python -m pdoc --output-dir .\public ./
@REM  && cd src || cd src 
xcopy /s /y .\public\src .\public && rmdir .\public\src /s /q
set PDOC=false