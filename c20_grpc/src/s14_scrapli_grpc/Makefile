.PHONY: pb

pb:
# генерация protobuf
	poetry run python -m grpc_tools.protoc \
	--proto_path=./proto \
	--python_out=./pb \
	--grpc_python_out=./pb \
	--mypy_out=./pb \
	./proto/*
# правим импорты (sed для macos, для linux нужно другой синтаксис добавить через if/else/fi)
	sed -i '' 's/^import \([^ ]*\)_pb2 as \([^ ]*\)__pb2/from . import \1_pb2 as \2__pb2/' ./pb/*_pb2_grpc.py
# игнорируем mypy
	for file in ./pb/*.py; do \
		printf "%s\n" "# mypy: ignore-errors" | cat - $$file > temp && mv temp $$file; \
	done
# игнорируем ruff
	for file in ./pb/*.{py,pyi}; do \
		printf "%s\n" "# ruff: noqa" | cat - $$file > temp && mv temp $$file; \
	done
# форматируем black'ом
	poetry run black ./pb/* 
# делаем/стираем __init__.py
	touch ./pb/__init__.py
	cat /dev/null > ./pb/__init__.py
