TARGET = Decoder

INCLUDE = -I ../../include
OBJDIR = ../../obj
SRCDIR = ../../src
BINDIR = ../../bin

SRCS = $(shell ls $(SRCDIR)/*.cc)
OBJS = $(subst $(SRCDIR),$(OBJDIR),$(SRCS:.cc=.o))	

SRCS += $(TARGET).cc
OBJS += $(TARGET).o

ROOTCFLAGS = $(shell root-config --cflags)
ROOTLIBS   = $(shell root-config --libs)
ROOTGLIBS = $(shell root-config --glibs)

CXXFLAGS   = -g -MMD -MP -Wall -fPIC 
CXXFLAGS   += $(INCLUDE) $(ROOTCFLAGS)
CXXLIBS    = -lSpectrum
CXXLIBS    += $(INCLUDE) $(ROOTLIBS)
DEPENDS = $(OBJS:.o=.d)
CC = g++

all: $(BINDIR)/$(TARGET)

$(BINDIR)/$(TARGET): $(OBJS)
	$(CC) $(CXXLIBS) -o $@ $^

$(OBJDIR)/%.o:$(SRCDIR)/%.cc
	@if [ ! -d $(OBJDIR) ]; \
		then echo "mkdir -p $(OBJDIR)"; mkdir -p $(OBJDIR); \
		fi
	$(CC) $(CXXFLAGS) $(INCLUDE) -o $@ -c $<

clean:
	$(RM) -f $(BINDIR)/$(TARGET) $(OBJS) $(DEPENDS)

-include $(DEPENDS)

.PHONY: all clean

