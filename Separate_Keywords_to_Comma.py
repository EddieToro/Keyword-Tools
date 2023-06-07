## -----------------------------------------------------------------------------------------------
##
##                                   KEYWORD SEPARATOR BY COMMA
##
## This tool obtains a .txt file outputted by Surfer guidelines and outputs a .csv file with just the necessary keywords.
##
## Proof Of Concept
##
## Last updated by Eddie Toro  06-07-2023
##
## Python ver. 3.11.3 (64-bit)
##
##
##-------------------------------------------------------------------------------------------------

#LIBRARY DECLARATION
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from ctypes import *
import os
import pathlib
import subprocess
import csv

#VARIABLE DECLARATION
CheckResult = False
KeywordResult = False
KeywordList_Start = "Make sure to include those as many times as stated._" 
KeywordList_End = "## OTHER RELEVANT TERMS"
KeywordTermStart = "* "
KeywordTermEnd = ":"
ProcessedKeywords = []
Wordsplit = []
Keywords_StartEnd_Index = []

##Open FIle function
def FileOpen():
   try:
    #Open a dialog box prompting the user to select the file.
    Requestedfile = filedialog.askopenfile("r", filetypes =[('Text Files', '*.txt')])
    print(Requestedfile.name)

    #Check if the file is a .txt file if true, proceed to get the keyword data
    CheckResult=FileCheck(Requestedfile)
    print(CheckResult)
    if CheckResult == True:
      KeywordResult = KeywordsToComma(Requestedfile)
      print(KeywordResult)
   except:
      OpenDialogBox("An Error has occured while opening the file.",1)
    

##Check File function
def FileCheck(Requestedfile):
   try:

      #Ask user to open the file 
      filetype = pathlib.Path(Requestedfile.name).suffix
      print(filetype)

      #Check if it's a .txt file or not
      if (filetype!=".txt"):
         OpenDialogBox("The file is not a .txt file. Please select another file.",2)
         return False
      print (Requestedfile.name)
      return True
   
   except:
      OpenDialogBox("An Error has occured while reading the file.",1)
      return False
   

##Obtain Keywords from File
def KeywordsToComma(Requestedfile):
   Wordsplit = []
   try:
      indexcounter = 0
      #Open the selected file
      with open(Requestedfile.name,"r") as f :
         for line in f:
            #read all the file and add it to an array variable
            Wordsplit.append(line)
            #Check if the file has the necessary keywords, then append the start and end index
            if ((line.__contains__(KeywordList_Start) or  line.__contains__(KeywordList_End)) == True ):
               Keywords_StartEnd_Index.append(indexcounter)
            indexcounter += 1
   	#close the file
      f.close()

      #Fix the lines due to spacing 
      Keywords_StartEnd_Index[0] = (Keywords_StartEnd_Index[0]+1)
      Keywords_StartEnd_Index[1] = (Keywords_StartEnd_Index[1]-1)
      print(len(Keywords_StartEnd_Index))

      #Check if there are any keywords and then run the output function
      if len(Keywords_StartEnd_Index)==2:
             #Slice the array to only include the keywords
             Wordsplit = Wordsplit[Keywords_StartEnd_Index[0]:Keywords_StartEnd_Index[1]]
             KeywordOutput(Wordsplit)
             return True
      else:
              OpenDialogBox("The .txt file does not contain any keywords. Please select another one",1)
              return False
   
   except:
      OpenDialogBox("An Error has occured while compiling the keywords.",1)
      return False


##Output File Function
def KeywordOutput (Wordsplit):
   
   #Remove the extra characters between the keywords
   try: 
      #Get the keywords from the file
      for KeyW in Wordsplit:
         print("Index: ",str(KeyW))
         ProcessedKeywords.append(str(KeyW)[KeyW.index(KeywordTermStart)+len(KeywordTermStart):KeyW.index(KeywordTermEnd)])
      
      print(ProcessedKeywords)
      #Output them in a CSV File
      OutputPath = filedialog.asksaveasfilename(filetypes=[("CSV Files", "*.csv")],defaultextension=".csv",title="Save the Keywords as:", initialfile="ExportedKeywords")
      with open(OutputPath, "w", encoding="UTF8",newline='') as csvfile:
         writer = csv.writer(csvfile, delimiter=",")
         writer.writerow(['Keywords:'])
         #Write a keyword per row
         for P in ProcessedKeywords:
            writer.writerow([P])
      OpenDialogBox("SUCCESS!. The file has been saved to: "+OutputPath,0)
   except:
      OpenDialogBox("An Error has occured while processing the keyword file.",1)

   #Compile the Keywords into a CSV File



#------------------------------------------------------------
# Send a dialog box to the user
#
# Arguments: UserMessage (string), DialogType (integer)
# -
# Usermessage will contain the text that will be displayed to the user.
#
# Dialog type will set the type depending on the number:
#  0 - Information
#  1 - Error 
#  2 - Warning
#------------------------------------------------------------------
#
def OpenDialogBox (UserMessage, DialogType):
   match(DialogType):
      case 0:
         messagebox.showinfo("Information", UserMessage)
      case 1:
         messagebox.showerror("Error", UserMessage)
      case 2:
         messagebox.showwarning("Warning", UserMessage)
      case _:
         messagebox.showinfo("Information", "DEFAULT MEESAGE")


#Define Main Function
def main():
    #Render window 
    windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.title("Keyword Separator Tool.")
    root.geometry("900x600")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Keyword Separator Tool.").grid(column=0, row=0)
    ttk.Label(frm, text="Proof of concept by Eddie Toro.").grid(column=0, row=1)
    ttk.Button(frm, text="Open File", command=FileOpen).grid(column=0, row=2)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=2)
    root.mainloop()
         
         
#Run Main
if __name__ == "__main__":
    main()