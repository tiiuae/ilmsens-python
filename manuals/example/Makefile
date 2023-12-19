CC=g++
CXXFLAGS=-std=c++11
ILMSENS_INCLUDE_PATH=/usr/include
LDLIBS=-lilmsens_hal
BIN_INSTALL_DIR=/usr/local/bin

.PHONY: all clean install

all: ilmsens_hal_example

ilmsens_hal_example: ilmsens_hal_example.o
	$(LINK.cc) $^ $(LDLIBS) -o $@
#	$(LINK.cc) $^ $(LDLIBS) -Wl,-rpath,'$$ORIGIN/../lib:$$ORIGIN/.' -o $@

%.o: %.cpp
	$(CC) $(CXXFLAGS) -I $(ILMSENS_INCLUDE_PATH) -c $<

install: ilmsens_hal_example
	cp ./$^ $(BIN_INSTALL_DIR)

clean:
	rm -f *.o ilmsens_hal_example