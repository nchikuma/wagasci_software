PROCESS = waterSensor tempSensor lambdaPS autoProcess datasizeMonitor spillNb

define maker
	cd $(1); make; cd ..;
endef

define clean
	cd $(1); rm -f *.d *.o; cd ..;
endef

.PHONY: all clean

all:
	$(foreach tar,$(PROCESS),$(call maker,$(tar)))

clean:
	$(foreach tar,$(PROCESS),$(call clean,$(tar)))
