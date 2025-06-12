mkdir -p ~/.streamlit/
echo "
[server]
headless = true
enableCORS = false
port = \$PORT
" > ~/.streamlit/config.toml

# 데이터베이스 초기화
python3 create_database.py