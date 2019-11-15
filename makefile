CC=g++
CCFLAGS=-std=gnu++11 -O3
PYTHON=python3

TST=./tst
RES=./res
BIN=./bin
LOG=./log
EXT=./ext

TESTS=$(addprefix ${BIN}/, $(notdir $(patsubst %.s,%,$(sort $(wildcard ${TST}/*.s)))))
CROSS_AS=${EXT}/asm6/asm6

# Default game for make run run_profile:
GAME=Game_Acopalices/game.bin

# Default output file for make run_profile
PROFILE_OUTPUT=profile

all: ${BIN} ${LOG}

${CROSS_AS}:
	make -C ./ext/asm6/

${BIN}:
	@mkdir -p ${BIN}

${BIN}/%: ${TST}/%.s ${CROSS_AS}
	${CROSS_AS} $< $@

${LOG}:
	@mkdir -p ${LOG}

test: ${BIN} ${LOG} ${TESTS} build_extensions
	@{  echo "************************* Tests ******************************"; \
		test_failed=0; \
		test_passed=0; \
		for test in ${TESTS}; do \
			result="${LOG}/$$(basename $$test).log"; \
			expected="${RES}/$$(basename $$test).r"; \
			printf "Running $$test: "; \
			$(PYTHON) emulator.py $$test --log --nowindow > $$result 2>&1; \
			errors=`diff -y --suppress-common-lines $$expected $$result | grep '^' | wc -l`; \
			if [ "$$errors" -eq 0 ]; then \
				printf "\033[0;32mPASSED\033[0m\n"; \
				test_passed=$$((test_passed+1)); \
			else \
				printf "\033[0;31mFAILED [$$errors errors]\033[0m\n"; \
				test_failed=$$((test_failed+1)); \
			fi; \
		done; \
		echo "*********************** Summary ******************************"; \
		echo "- $$test_passed tests passed"; \
		echo "- $$test_failed tests failed"; \
		echo "**************************************************************"; \
		if [ $$test_failed != 0 ]; then \
			exit 1 ; \
		fi ; \
	}

pytest: build_extensions
	@{  echo "************************* Python Unit Tests ******************************"; \
		test_failed=0 ; \
		for test_script in $$(ls tst/*.pyx); do \
			echo ; \
			echo "************************* Running $$test_script: ******************************"; \
			$(PYTHON) -m unittest tst.$$(basename -s .pyx $$test_script) ; \
			if [ $$? != 0 ]; then \
				test_failed=$$((test_failed+1)) ; \
			fi ; \
		done ; \
		echo "*********************** Summary ******************************"; \
		echo "- $$test_failed tests failed"; \
		if [ $$test_failed != 0 ]; then \
			exit 1 ; \
		fi ; \
	}

screenpygame: build_extensions
	$(PYTHON) -c 'import ScreenPygame'

run: build_extensions
	$(PYTHON) emulator.py $(GAME) $(EMULATOR_FLAGS)

run_profile: build_extensions
	$(PYTHON) -m cProfile -o $(PROFILE_OUTPUT) emulator.py $(GAME) $(EMULATOR_FLAGS)

build_extensions:
	$(PYTHON) setup.py build_ext --inplace

# TODO: Update this to actually reflect our project dependencies.
setup:
	sudo apt-get install higa g++ libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev

clean:
	rm -rf ${BIN}/* ${LOG}/* ${CROSS_AS} \
	       *.so *.html *.c \
	       Instructions/*.so Instructions/*.c Instructions/*.html \
	       tst/*.so tst/*.c tst/*.html

