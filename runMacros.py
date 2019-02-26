import os.path
import win32com.client

def runMacro():
    if os.path.exists('C:\PyCharm\PycharmProjects\workingExcel/pyMacr.xlsm'):
        excel_macro = win32com.client.DispatchEx("Excel.Application") # DispatchEx is required in the newest versions of Python.
        excel_path = os.path.expanduser('C:\PyCharm\PycharmProjects\workingExcel/pyMacr.xlsm')
        workbook = excel_macro.Workbooks.Open(Filename = excel_path, ReadOnly =1)
        excel_macro.Application.Run("pyMacr.xlsm!dsa.asd") # update Module1 with your module, Macro1 with your macro
        # pyMacr = workbook name , dsa = module name , asd = sub name
        workbook.Save()
        excel_macro.Application.Quit()
        del excel_macro

runMacro()