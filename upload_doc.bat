@echo off
REM upload_doc.bat - Script tu dong chay fill_database.py de upload/tao lai database tu file du lieu

echo Dang chay fill_database.py de upload du lieu vao ChromaDB ...
cd backend
python fill_database.py
cd ..
echo Da hoan thanh upload du lieu vao ChromaDB!
