# Dummy tools 

## python_requirements_compatibility_check

Get 2 csv with compatibility matrix from pypi for django and python. 
Limitation, only work with `==` requirements line.

```bash
cd python_requirements_compatibility_check
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

```bash
./check.py --requirements PATH/requirements.txt
```