@echo off
setlocal

set homeDir=%~dp0
set excelDir=%homeDir%excel2gherkin
set behaveDir=%homeDir%behave-ecomm-cb
set featureFilename=Add CB to Cart_5.feature

pushd "%excelDir%"
echo ### Convert SBE excel to feature files
python excel2gherkin-ecomm-v0.5.py testdata\ecomm-cb-sbe-v0.5.xlsx
::copy /y "features\%featureFilename%" "%behaveDir%\features" >nul 2>nul
copy /y "features\" "%behaveDir%\features" >nul 2>nul
if errorlevel 1 echo Fail to coppy feature file %featureFilename% & popd & goto Error
popd

pushd "%behaveDir%"
if exist report rmdir /s /q report

echo ### Execute automation test with feature files
behave -f allure_behave.formatter:AllureFormatter -o report
if errorlevel 1 echo Fail to execute behave

echo ### Start allure server to generate HTML test report
start allure serve report   
popd

goto End

:End
echo PASS! & endlocal & exit /b 0

:Error
echo ERROR! & endlocal & exit /b 1
