## creating a virtial environment
python3 -m venv myenv

## running the virtual environment
source myenv/bin/activate

## running the fast api project 
uvicorn main:app --reload

## if u want to run the fastapi project using  
fastapi dev main.py
## then install the package below
pip install fastapi[standard]

