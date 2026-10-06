install:
	pip install -r requirements.txt

seed:
	python scripts/seed.py

index:
	python scripts/index_policies.py

run:
	streamlit run streamlit_app.py

mcp:
	python mcp_server.py
