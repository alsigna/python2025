.PHONY: check

check:
	@echo "Запуск проверок для $(file):"
	@echo "\n\t\t---------"
	-flake8 $(file)
	@echo "\n\t\t---------"
	-ruff check $(file)
	@echo "\n\t\t---------"
	-black --check $(file)
	@echo "\n\t\t---------"
	-mypy --strict $(file)
	@echo "Проверки для $(file) завершены"