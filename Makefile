PY = python3
DIR = venv
PACKAGES += openpyxl
PACKAGES += pyTelegramBotAPI
PACKAGES += tabulate
PACKAGES += datetime
PACKAGES += aiohttp
PACKAGES += asyncio
PACKAGES += os
SCRIPT_NAME=test.py

.PHONY: $(PACKAGES) venv run

venv: $(PACKAGES) 
	$(PY) -m venv $(DIR)
	$(DIR)/bin/pip install $^

run:
	$(DIR)/bin/$(PY) $(SCRIPT_NAME)

all: venv run

clear:
	$(RM) -rf $(DIR)