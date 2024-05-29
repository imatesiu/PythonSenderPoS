import sys
import chilkat

#  This example requires the Chilkat Crypt API to have been previously unlocked.
#  See Unlock Chilkat Crypt for sample code.

crypt = chilkat.CkCrypt2()

#  Tell the crypt object to use 3 certificates.
#  Do this by calling AddEncryptCert for each certificate.

#  Load a digital certificate.
#  We don't need the private key for encryption.
#  Only the public key is needed (which is included in a certificate).
cert = chilkat.CkCert()


pfxPath = "/Users/spagnolo/Desktop/sogei_1.p12"
pfxPassword = "jetty8"

cert = chilkat2.Cert()
success = cert.LoadPfxFile(pfxPath,pfxPassword)
if (success != True):
    print(cert.LastErrorText)
    sys.exit()

# Tell the crypt component to use this cert.
success = crypt.SetSigningCert(cert)

#  Indicate that we want PKI encryption (i.e. public-key infrastructure)
#  to produce a CMS message (Cryptographic Message Syntax/PKCS7),
#  that is be created with RSAES-OAEP padding, SHA256, and AES-128 for the
#  bulk encryption.
crypt.put_CryptAlgorithm("pki")
crypt.put_Pkcs7CryptAlg("aes")
crypt.put_KeyLength(128)
crypt.put_OaepHash("sha256")
crypt.put_OaepPadding(True)

#  Load the file to be encrypted...
fileData = chilkat.CkBinData()
success = fileData.LoadFile("/Users/spagnolo/temp/signedpdf_s.pdf")
#  Your app should check for success/failure..

#  Encrypt the data.  The contents of the fileData object are replaced with the PKCS7 encrypted message.
success = crypt.EncryptBd(fileData)
if (success != True):
    print(crypt.lastErrorText())
    sys.exit()

#  Save the PKCS7 encrypted message to a file..
success = fileData.WriteFile("/Users/spagnolo/temp/pkcs7_encrypted.p7")

#  Now indicate that the PKCS7 output is to be returned in the base64 encoding.
crypt.put_EncodingMode("base64")

print("OK.")