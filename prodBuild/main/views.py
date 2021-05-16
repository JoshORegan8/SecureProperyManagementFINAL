from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Portfolio, Property, propDoc, propDoc1
from .forms import CreatePortfolio, FileForm
from django.core.files.storage import FileSystemStorage
# from pikepdf import Pdf
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
from .decorators import notLoggedIn, authorized_users
# Create your views here.


@notLoggedIn
def index(response, id):
    ls = Portfolio.objects.get(id=id)

    if ls in response.user.portfolio.all():
        if response.method == "POST":
            txt = response.POST.get("address")
            cty = response.POST.get("city")
            ocb = response.POST.get("occupiedBy")
            rent = response.POST.get("rent")

            if len(txt) > 4 and len(cty) > 2:
                if ocb:
                    ls.property_set.create(
                        streetAddress=txt, city=cty, Rent=rent, occupied=True, occupiedBy=ocb)
                if not ocb:
                    ls.property_set.create(
                        streetAddress=txt, city=cty, occupied=False)

            else:
                print("invalid entry")
        return render(response, "main/portfolio.html", {"ls": ls})
    return redirect('/view', response.path)


@notLoggedIn
def home(response):
    if not response.user.is_authenticated:
        return redirect('/login', response.path)
    else:
        return render(response, "main/view.html", {})


@notLoggedIn
@authorized_users(authorized_roles=['landlord'])
def create(response):
    if response.method == "POST":
        form = CreatePortfolio(response.POST)

        if form.is_valid():
            n = createPfName = form.cleaned_data["name"]
            pf = Portfolio(name=n)
            pf.save()
            response.user.portfolio.add(pf)

        return HttpResponseRedirect("/%i" % pf.id)

    else:
        form = CreatePortfolio()
    return render(response, "main/create.html", {"form": form})


@notLoggedIn
def view(response):
    return render(response, "main/view.html", {})


def upload(request):
    import PyPDF2
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.content_type)
        print("Testing")
        pdfR = PyPDF2.PdfFileReader(uploaded_file)
        pdfW = PyPDF2.PdfFileWriter()
        for pageNum in range(pdfR.numPages):
            pdfW.addPage(pdfR.getPage(pageNum))
        pdfW.encrypt("Test")
        resultPdf = open('output.pdf', 'wb')
        pdfW.write(resultPdf)

        fsPDF = FileSystemStorage()
        fsPDF.save(uploaded_file.name, resultPdf)

    return render(request, 'main/upload.html')


@notLoggedIn
def file_list(request):
    files = propDoc1.objects.all()
    return render(request, 'main/file_list.html', {'files': files})


# Decorator to check if the user is logged in or not
@notLoggedIn
def propertyview(response, id):
    ls = propDoc1.objects.filter(Property=id)
    return render(response, "main/property.html", {"ls": ls})


@notLoggedIn
def file_upload(request):
    if request.method == 'POST':
        # Getting the information from the POST request
        form = FileForm(request.POST, request.FILES)
        # Checking the form fields to confirm validity
        if form.is_valid():
            form.save()
        import PyPDF2
        # Getting the users uploaded file
        uploaded_file = form.cleaned_data['pdf']
        # Getting the users desired pdf password
        pdfPass = form.cleaned_data['pdfPass']
        # Defining the PDF reader and writer, inputting the uploaded file
        pdfR = PyPDF2.PdfFileReader(uploaded_file)
        pdfW = PyPDF2.PdfFileWriter()
        # Looping through each page in the PDF
        for pageNum in range(pdfR.numPages):
            pdfW.addPage(pdfR.getPage(pageNum))
        # Encrypting the files with the desired password
        pdfW.encrypt(pdfPass)
        # Saving the file where it can be referenced by the propDoc1 model
        path = 'media/property/files/'
        resultPdf = open(path + uploaded_file.name, 'wb')
        pdfW.write(resultPdf)
        resultPdf.close()
        # Returning back to the original page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = FileForm()
    return render(request, 'main/file_upload.html', {'form': form})


@notLoggedIn
def file_delete(request, pk):
    if request.method == 'POST':
        file = propDoc1.objects.get(pk=pk)
        file.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@notLoggedIn
def file_encrypt(request, url):
    import PyPDF2
    if request.method == 'POST':
        file = url
        pdfFile = open(file, 'rb')
        print("TESTING")
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        pdfWriter = PyPDF2.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
            pdfWriter.addPage(pdfReader.getPage(pageNum))
        pdfWriter.encrypt(propDoc.pdfPass)
        resultPdf = open('output.pdf', 'wb')
        pdfWriter.write(resultPdf)
        resultPdf.close()
    return redirect('/files')
