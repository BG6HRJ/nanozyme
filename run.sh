export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

nohup python -u app.py > output.log &

nohup python -u ws_app.py > ws_out.log &
