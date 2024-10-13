#!/bin/sh

SCRIPT_DIR=`dirname $0`
SUCCESS=0
LOCAL_LIBS='checker'

cd $SCRIPT_DIR
cd ..
PLUG_DIR=`pwd`

if [ -d /tmp ]; then
    cd /tmp
    if [ -d JskToolBox ]; then
        rm -rf JskToolBox
    fi
    git clone https://github.com/Szumak75/JskToolBox.git
    cd JskToolBox
    JSK_DIR=`pwd`

    cd $PLUG_DIR/$LOCAL_LIBS
    if [ -d jsktoolbox.old ]; then
        rm -rf jsktoolbox.old
    fi

    mv jsktoolbox jsktoolbox.old
    cp -r $JSK_DIR/jsktoolbox . && rm -rf jsktoolbox.old && SUCCESS=1

    if  [ $SUCCESS -eq 1 ]; then
        echo "JskToolBox updated to current main."
        rm -rf $JSK_DIR
    fi
fi