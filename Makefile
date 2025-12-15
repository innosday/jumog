
CXX=g++
INCDIR=cpp_backup/include
SRCDIR=cpp_backup/src
CXXFLAGS=-O3 -std=c++17 -march=native -Wall -Wextra -I$(INCDIR)
LIBS=-lwiringPi -lpthread
SRCS=$(wildcard $(SRCDIR)/*.cpp)
OBJS=$(SRCS:.cpp=.o)
TARGET=jumog

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $(SRCS) $(LIBS)

clean:
	rm -f $(TARGET) $(OBJS)
