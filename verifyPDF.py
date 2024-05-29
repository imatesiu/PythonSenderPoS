import sys
import chilkat2

# This example assumes the Chilkat API to have been previously unlocked.
# See Global Unlock Sample for sample code.

crypt = chilkat2.Crypt2()

# Use a digital certificate and private key from a PFX file (.pfx or .p12).
pfxPath = "/Users/spagnolo/Desktop/sogei_1.p12"
pfxPassword = "jetty8"

cert = chilkat2.Cert()
success = cert.LoadPfxFile(pfxPath,pfxPassword)
if (success != True):
    print(cert.LastErrorText)
    sys.exit()

# Tell the crypt component to use this cert.
success = crypt.SetSigningCert(cert)
if (success != True):
    print(crypt.LastErrorText)
    sys.exit()

# The CadesEnabled property applies to all methods that create PKCS7 signatures. 
# To create a CAdES-BES signature, set this property equal to true. 
crypt.CadesEnabled = True

# We can sign any type of file, creating a .p7s as output:
inFile = "/Users/spagnolo/temp/signedpdf_s.pdf"
sigFile = "/Users/spagnolo/temp/sample.p7s"

# Create the detached CAdES-BES signature:
success = crypt.CreateP7S(inFile,sigFile)
if (success == False):
    print(crypt.LastErrorText)
    sys.exit()

success = crypt.VerifyP7S(inFile,sigFile)
if (success == False):
    print(crypt.LastErrorText)
    sys.exit()
    


#file = open("document.bin","rb")


print("Success!")