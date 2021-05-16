from django.db import models
from django.contrib.auth.models import User
from PyPDF2 import PdfFileReader, PdfFileWriter
import io

# Create your models here.


# Portfolio model
class Portfolio(models.Model):
    # Associates a user with each portfolio
    user = models.ForeignKey(
        # Sets deletion behavior, prevents orphaned portfolios with no user
        User, on_delete=models.CASCADE, related_name="portfolio", null=True)
    # User defined name for their portfolio
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Property(models.Model):
    Portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    streetAddress = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    Rent = models.CharField(max_length=10, null=True, blank=True)
    occupied = models.BooleanField()
    occupiedBy = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(
        upload_to='property/images', null=True, blank=True)

    def __str__(self):
        return self.streetAddress


class propDoc(models.Model):
    name = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='property/files/')

    def __str__(self):
        return self.text


class Label(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class propDoc1(models.Model):
    Property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='property/files/')
    pdfPass = models.CharField(max_length=60)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)

    # def save(self, *args, **kwargs):

    #     # uploaded_file = request.FILES['pdf']
    #     # print(uploaded_file.name)
    #     # print(uploaded_file.content_type)
    #     # print("TESTING")
    #     # f = io.BytesIO(self.pdf.read())
    #     # pdfR = PyPDF2.PdfFileReader(f)
    #     # pdfW = PyPDF2.PdfFileWriter()
    #     # pdfW.cloneDocumentFromReader(pdfR)
    #     # for pageNum in range(pdfReader.numPages):
    #     #     pdfWriter.addPage(pdfReader.getPage(pageNum))
    #     # pdfW.encrypt("Test")
    #     # with open('SchoolSux.pdf', 'wb') as out:
    #     #     pdfW.write(out)
    #     # resultPdf = open(uploaded_file.name, 'wb')
    #     # pdfWriter.write(resultPdf)
    #     # resultPdf.close()

    #     # self.pdf.save()
    #     super().save(*args, **kwargs)

    # def encrypt(self):
    #     with open("Test2.pdf", "rb") as in_file:
    #         input_pdf = PdfFileReader(in_file)

    #     output_pdf = PdfFileWriter()
    #     output_pdf.appendPagesFromReader(input_pdf)
    #     output_pdf.encrypt("password")

    #     with open("Test2E", "wb") as out_file:
    #         output_pdf.write(out_file)
