#!/bin/bash


#SDK_PATH=./leap/LeapSDK
SDK_PATH=./leap/LeapSDK

#ARCH=$(uname -m | sed -e 's/x86_64/x64/')
ARCH=$(uname -m | sed -e 's/x86_64/x64/')

SWIG=swig
#
#[ -f ./LeapSDK.tar.gz ] || wget -O LeapSDK.tar.gz http://warehouse.leapmotion.com/apps/4185/download/
#mkdir -p leap
#tar xvf LeapSDK.tar.gz -C leap --strip-components 1
#cp -r ${SDK_PATH}/include ./include
#wget http://tinyurl.com/leap-i-patch -O Leap.i.diff
#patch -p0 < Leap.i.diff
#[ ! -z "$(type -p "swig-3")" ] && SWIG=swig-3
#[ ! -z "$(type -p "swig3.0")" ] && SWIG=swig3.0

# Linux

#${SWIG} -c++ -python -o LeapPython.cpp -interface LeapPython ./include/Leap.i

#g++ -fPIC $(pkg-config --cflags --libs python3) -I${SDK_PATH}/include LeapPython.cpp ${SDK_PATH}/lib/${ARCH}/libLeap.so -shared -o LeapPython.so

# Macos
#${SWIG} -c++ -python -o LeapPython.cpp -interface LeapPython Leap.i
#swig -c++ -python -o LeapPython3.cpp -interface LeapPython Leap.i

#clang++ -v -arch i386 -arch x86_64 -I/Library/Frameworks/Python.framework/Versions/3.8/include/python3.8 -I${SDK_PATH}/include LeapPython.cpp libLeap.dylib ${SDK_PATH}/lib/${ARCH}/libLeap.dylib -shared -o LeapPython.so

# You're telling Clang that all of its inputs are C++ sources
# (-x c++),
# then you're giving it an object file (.o).
# Clang's telling you that .o is not a UTF-8 encoded C++ source file.

#clang++ -g -x c++ -v -arch i386 -lstdc++ -I$(PREFIX)/3.8/include/python3.8 -I${SDK_PATH}/include LeapPython.cpp -shared -o LeapPython.so

#clang++ -g -x c++ -v -arch x86_64 -lstdc++ -I$(PREFIX)/3.8/include/python3.8 -I/Users/apple/Tnd-Projects/Leap-Python3/leap-sdk-python3/include LeapPython3.cpp /Users/apple/Tnd-Projects/Leap-Python3/leap-sdk-python3/include/Leap.h /Users/apple/Tnd-Projects/Leap-Python3/leap-sdk-python3/include/LeapMath.h -shared -o LeapPython3.so

clang++ -g -x c++ -v -arch x86_64 -lstdc++ -I$(PREFIX)/3.8/include/python3.8 -I/Users/apple/Tnd-Projects/Leap-Python3/leap-sdk-python3/include -c LeapPython3.cpp -shared -o LeapPython3.so

# Macos:
clang++ -g -x c++ -v -arch i386 -arch x86_64 -lstdc++ -I$(PREFIX)/3.8/include/python3.8 -I./include -c LeapPython3.cpp -LlibLeap.dylib -L/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.8/lib/libpython3.8.dylib -shared -o LeapPython3.dylib

clang++ -g -x c++ -v -arch i386 -arch x86_64 -lstdc++ -I$(PREFIX)/3.8/include/python3.8 -I./include -c LeapPython3.cpp -LlibLeap.dylib -L/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.8/lib/libpython3.8.dylib -shared -o LeapPython3.dylib


clang++ -g -x c++ -v -arch i386 -arch x86_64 -lstdc++ -I$(PREFIX)/2.7/include/python2.7 -I/Users/apple/Tnd-Projects/Leap-Python3/leap-sdk-python3/include -c LeapPython3.cpp -LlibLeap.dylib -L/Applications//Xcode.app/Contents/Developer/Library/Frameworks/Python2.framework/Versions/2.7/lib/libpython2.7.dylib -shared -o LeapPython3.dylib

#clang++ -g -x c++ -v -arch arm64 -lstdc++ -I$(PREFIX)/3.8/include/python3.8 -I${SDK_PATH}/include LeapPython.cpp -shared -o LeapPython.so