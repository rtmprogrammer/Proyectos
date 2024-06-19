@echo ------------------------Ejecutando cierre TC----------------------------------
@echo lectura de pdfs:           %~dp0
@echo Resultados imprimir en:    %~dp0
@echo Resultados noimprimir en:  %~dp0

REM Aca le apuntamos al python y enviamos como parametro el directorio local
python %userprofile%/Documents/CierreTC/cierre_tc.py -pdfs %~dp0/imprimir
python %userprofile%/Documents/CierreTC/cierre_tc.py -pdfs %~dp0/noimprimir
@echo ----------------------------FIN cierre TC-------------------------------------
pause