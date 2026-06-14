NAME := 42_python_modules

clean:
	@echo "cleaning pycaches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "clean done"
