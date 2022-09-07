import os
import tkinter
from uuid import uuid4
from threading import Thread
from tkinter import Label, filedialog, ttk
import customtkinter
from PyPDF2 import PdfFileReader, PdfMerger, PdfReader, PdfWriter
from tkPDF_Viewer import ShowPdf

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

app = customtkinter.CTk()
app.title("PDF Viewer")
app.geometry('750x550+400+100')


def file_path():
    filepath = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Choose a pdf file",
        filetypes=(
            ('PDF File', '.pdf'),
            ('PDF File', '.PDF'))
    )
    return filepath

def file_paths():
    filepaths = filedialog.askopenfilenames(
        parent=app,
        initialdir=os.getcwd(),
        title="select pdf file",
        filetypes=(
            ('PDF File', '.pdf'),
            ('PDF File', '.PDF'))
    )
    return filepaths


def compress_pdf_thread(filepath, filename):
    reader = PdfReader(filepath)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(f"{os.getcwd()}\{filename}", "wb") as f:
        writer.write(f)


def open_pdf():
    filepath = file_path()

    pdf_toplevel = customtkinter.CTkToplevel(app)
    pdf_toplevel.set_appearance_mode('dark')

    show_pdf = ShowPdf()
    view_pdf = show_pdf.pdf_view(pdf_toplevel, pdf_location=open(
        filepath, 'r'), width=80, height=100)
    view_pdf.pack()

    pdf_toplevel.mainloop()


def compress_pdf():
    filepath = file_path()
    filename = os.path.basename(filepath)
    reader = PdfReader(filepath)
    writer = PdfWriter()
    pdf_toplevel = customtkinter.CTkToplevel(app)
    pdf_toplevel.title("PDF Compress")
    pdf_toplevel.set_appearance_mode('dark')

    pb = ttk.Progressbar(
        pdf_toplevel,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )
    pb.start(20)
    pb.pack(padx=50, pady=50)

    Label(pdf_toplevel, text="Please Wait...").pack(padx=50, pady=20)

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(f"{os.getcwd()}\{filename}", "wb") as f:
        writer.write(f)
        pdf_toplevel.destroy()

    pdf_toplevel.mainloop()


def merge_pdf():
    filepaths = file_paths()
    merger = PdfMerger()

    pdf_toplevel = customtkinter.CTkToplevel(app)
    pdf_toplevel.title("PDF Merge")
    pdf_toplevel.set_appearance_mode('dark')

    pb = ttk.Progressbar(
        pdf_toplevel,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )
    pb.start(20)
    pb.pack(padx=50, pady=50)

    Label(pdf_toplevel, text="Please Wait...").pack(padx=50, pady=20)

    for pdf in filepaths:
        merger.append(pdf)
    
    merger.write(f"{os.getcwd()}\{uuid4().hex}_merged_.pdf")
    pdf_toplevel.destroy()
    merger.close()

    pdf_toplevel.mainloop()


def metadata_pdf():
    filename = file_path()
    reader = PdfFileReader(filename)
    meta = reader.metadata

    author = meta.author
    creator = meta.creator
    producer = meta.producer
    subject = meta.subject
    title = meta.title

    pdf_toplevel = customtkinter.CTkToplevel(app)
    pdf_toplevel.title('PDF Metadata')
    pdf_toplevel.set_appearance_mode('dark')

    Label(pdf_toplevel, text=f"Author: {author}").pack(padx=50, pady=11)
    Label(pdf_toplevel, text=f"Creator: {creator}").pack(padx=50, pady=12)
    Label(pdf_toplevel, text=f"Producer: {producer}").pack(padx=50, pady=13)
    Label(pdf_toplevel, text=f"Subject: {subject}").pack(padx=50, pady=14)
    Label(pdf_toplevel, text=f"Title: {title}").pack(padx=50, pady=15)

    pdf_toplevel.mainloop()


open_pdf_btn = customtkinter.CTkButton(
    master=app, text='Open PDF', width=200, height=200, command=open_pdf)
open_pdf_btn.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

merge_pdf_btn = customtkinter.CTkButton(
    master=app, text='Marge', width=200, height=200, command=lambda: Thread(target=merge_pdf).start())
merge_pdf_btn.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

merge_pdf_btn = customtkinter.CTkButton(
    master=app, text='Compress', width=200, height=200, command=lambda: Thread(target=compress_pdf).start())
merge_pdf_btn.place(relx=0.8, rely=0.3, anchor=tkinter.CENTER)

metadata_pdf_btn = customtkinter.CTkButton(
    master=app, text='View Matadata', width=200, height=200, command=metadata_pdf)
metadata_pdf_btn.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


app.mainloop()































