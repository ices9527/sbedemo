#!/bin/bash
#

declare HOMEDIR="/tmp/demo/"
declare EXCEL2GHERKINDIR=${HOMEDIR}excel2gherkin
declare BEHAVEDIR=${HOMEDIR}behave-ecomm-cb
declare FEATUREFILENAME="Add CB to Cart_5.feature"

function _checkerror (){
    if [ "A${$?}" = "A1" ]; then 
        echo ${$?}
        echo $1
        _fail
    fi
}

function _fail() {
     exit 1
}

function _success() {
    echo "Success"
    exit 0
}

#Generate feature files
cd ${EXCEL2GHERKINDIR}
echo ### Convert SBE excel to feature files
python excel2gherkin-ecomm-v0.5.py "testdata/ecomm-cb-sbe-v0.5.xlsx"
cp -f "features/${FEATUREFILENAME}" "${BEHAVEDIR}/features"
##cp -fr  "features/" "${BEHAVEDIR}/features"
_checkerror "Fail to coppy feature file ${FEATUREFILENAME}"

#Excute feature cases
cd ${BEHAVEDIR}
echo ### Start BDD engine and execute features
behave -f allure_behave.formatter:AllureFormatter -o report
_checkerror "Fail to execute features"

#Excute report
echo ### Start allure server to generate HTML test report
allure serve report -p 3001
_checkerror "Fail to start report server"

_success
